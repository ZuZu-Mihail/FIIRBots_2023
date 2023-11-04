# imu.py Python driver for the InvenSense inertial measurement units
# This is the base class
# Adapted from Sebastian Plamauer's MPU9150 driver:
# https://github.com/micropython-IMU/micropython-mpu9150.git
# Authors Peter Hinch, Sebastian Plamauer
# V0.2 17th May 2017 Platform independent: utime and machine replace pyb

'''
mpu9250 is a micropython module for the InvenSense MPU9250 sensor.
It measures acceleration, turn rate and the magnetic field in three axis.
mpu9150 driver modified for the MPU9250 by Peter Hinch

The MIT License (MIT)
Copyright (c) 2014 Sebastian Plamauer, oeplse@gmail.com, Peter Hinch
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

#PORT FOR PYTHON #################### RASPBERRY 0 ##############

# User access is now by properties e.g.
# myimu = MPU9250('X')
# magx = myimu.mag.x
# accelxyz = myimu.accel.xyz
# Error handling: on code used for initialisation, abort with message
# At runtime try to continue returning last good data value. We don't want aircraft
# crashing. However if the I2C has crashed we're probably stuffed.

import time
from math import sqrt, atan2
import smbus                    #import SMBus module of I2C


class MPUException(OSError):
    '''
    Exception for MPU devices
    '''
    pass

def bytes_toint(msb, lsb):
    '''
    Convert two bytes to signed integer (big endian)
    for little endian reverse msb, lsb arguments
    Can be used in an interrupt handler
    '''
    if not msb & 0x80:
        return msb << 8 | lsb  # +ve
    return - (((msb ^ 255) << 8) | (lsb ^ 255) + 1)

def wrap(angle):
    while (angle > +180):
        angle -= 360
    while (angle < -180):
        angle += 360
    return angle

def angle_average(wa, a, wb, b):
	return wrap(wa * a + wb * (a + wrap(b-a)))

def ticks_ms():
    return int(time.time() * 1000)

def sleep_ms(ms):
    time.sleep(ms / 1000)

class MPU6050(object):
    '''
    Module for InvenSense IMUs. Base class implements MPU6050 6DOF sensor, with
    features common to MPU9150 and MPU9250 9DOF sensors.
    '''
    __bus = smbus.SMBus(1)
    
    #some MPU6050 Registers and their Address
    __PWR_MGMT_1   = 0x6B
    __SMPLRT_DIV   = 0x19
    __CONFIG       = 0x1A
    __GYRO_CONFIG  = 0x1B
    __INT_ENABLE   = 0x38
    __ACCEL_XOUT_H = 0x3B
    __ACCEL_YOUT_H = 0x3D
    __ACCEL_ZOUT_H = 0x3F
    __GYRO_XOUT_H  = 0x43
    __GYRO_YOUT_H  = 0x45
    __GYRO_ZOUT_H  = 0x47

    __DEVICE_ADDRESS = 0X68

    __CALIBRATION_MEASURES = 500

    __DEFAULT_ACCEL_COEFF = 0.02
    __DEFAULT_GYRO_COEFF = 0.98

    __ACCEL_TRANSFORMATION_NUMBER = 0.00006103515
    # __GYRO_TRANSFORMATION_NUMBER = 0.01525878906
    
    # UPDATED TRANSFORMATION NUMBER FOR THE SENSIVITY
    # __GYRO_TRANSFORMATION_NUMBER = 0.00855878906
    __GYRO_TRANSFORMATION_NUMBER = 0.00852878906

    __RAD_TO_DEG = 57.2957795131
    
    _rawAccX = 0
    _rawAccY = 0
    _rawAccZ = 0

    _rawGyroX = 0
    _rawGyroY = 0
    _rawGyroZ = 0
    
    _accX = 0
    _accY = 0
    _accZ = 0

    _angGyroX = 0
    _angGyroY = 0
    _angGyroZ = 0

    _angX = 0
    _angY = 0
    _angZ = 0

    __dt = 0
    __intervalStart = 0

    __gyroXOffset = 0
    __gyroYOffset = 0
    __gyroZOffset = 0

    __filterAccelCoeff = 0
    __filterGyroCoeff = 0

    def __init__(self, side_str=0X68):

        self.__DEVICE_ADDRESS = side_str

        self.__bus.write_byte_data(self.__DEVICE_ADDRESS, self.__SMPLRT_DIV, 7)

        self.__bus.write_byte_data(self.__DEVICE_ADDRESS, self.__PWR_MGMT_1, 1)

        self.__bus.write_byte_data(self.__DEVICE_ADDRESS, self.__CONFIG, 0)

        self.__bus.write_byte_data(self.__DEVICE_ADDRESS, self.__GYRO_CONFIG, 24)

        self.__bus.write_byte_data(self.__DEVICE_ADDRESS, self.__INT_ENABLE, 1)

    def Initialize(self):
        '''
        Start the MPU6050 and read data for the first time
        '''
        self.__filterAccelCoeff = self.__DEFAULT_ACCEL_COEFF
        self.__filterGyroCoeff = self.__DEFAULT_GYRO_COEFF

        self.accel_range = 0                    # default to highest sensitivity
        self.gyro_range = 0                     # Likewise for gyro

        self.__intervalStart = ticks_ms()

    def Calibrate(self):
        '''
        Do multiple reads and calculate the average error to be used
        for later calculations.
        '''
        sumGyroX = 0
        sumGyroY = 0
        sumGyroZ = 0

        i = 0
        while( i < self.__CALIBRATION_MEASURES):
            self._read_raw_data()
            sumGyroX += self._rawGyroX
            sumGyroY += self._rawGyroY
            sumGyroZ += self._rawGyroZ
            i+=1
            sleep_ms(1)
        
        sumGyroX /= self.__CALIBRATION_MEASURES
        sumGyroY /= self.__CALIBRATION_MEASURES
        sumGyroZ /= self.__CALIBRATION_MEASURES

        self.__gyroXOffset = sumGyroX
        self.__gyroYOffset = sumGyroY
        self.__gyroZOffset = sumGyroZ

    def read(self):
        '''
        Update the acceleration and gyroscope data of the MPU6050.\n
        TO AVOID UNREGISTERED MOVEMENT IT HAS TO BE CALLED CONTINUOUS.
        '''
        self._read_raw_data()

        accX = self._rawAccX * self.__ACCEL_TRANSFORMATION_NUMBER
        accY = self._rawAccY * self.__ACCEL_TRANSFORMATION_NUMBER
        accZ = self._rawAccZ * self.__ACCEL_TRANSFORMATION_NUMBER

        gyroX = (self._rawGyroX - self.__gyroXOffset) * self.__GYRO_TRANSFORMATION_NUMBER
        gyroY = (self._rawGyroY - self.__gyroYOffset) * self.__GYRO_TRANSFORMATION_NUMBER
        gyroZ = (self._rawGyroZ - self.__gyroZOffset) * self.__GYRO_TRANSFORMATION_NUMBER

        self._angAccX = wrap((atan2(accY, sqrt(accZ * accZ + accX * accX))) * self.__RAD_TO_DEG)
        self._angAccY = wrap((-atan2(accX, sqrt(accZ * accZ + accY * accY))) * self.__RAD_TO_DEG)
        
        self.__dt = ((ticks_ms() - self.__intervalStart)) * 0.001
        self._angGyroX = wrap(self._angGyroX + gyroX * self.__dt)
        self._angGyroY = wrap(self._angGyroY + gyroY * self.__dt)
        self._angGyroZ = wrap(self._angGyroZ + gyroZ * self.__dt)

        self._angX = angle_average(self.__filterAccelCoeff, self._angAccX, self.__filterGyroCoeff, self._angX + gyroX * self.__dt)
        self._angY = angle_average(self.__filterAccelCoeff, self._angAccY, self.__filterGyroCoeff, self._angY + gyroY * self.__dt)
        self._angZ = self._angGyroZ

        self.__intervalStart = ticks_ms()

    def _read(self, addr):
	#Accelero and Gyro value are 16-bit
        high = self.__bus.read_byte_data(self.__DEVICE_ADDRESS, addr)
        low = self.__bus.read_byte_data(self.__DEVICE_ADDRESS, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value
    
    def _read_raw_data(self):
        self._rawAccX = self._read(self.__ACCEL_XOUT_H)
        self._rawAccY = self._read(self.__ACCEL_YOUT_H)
        self._rawAccZ = self._read(self.__ACCEL_ZOUT_H)
    
	    #Read Gyroscope raw value
        self._rawGyroX = self._read(self.__GYRO_XOUT_H)
        self._rawGyroY = self._read(self.__GYRO_YOUT_H)
        self._rawGyroZ = self._read(self.__GYRO_ZOUT_H)
	