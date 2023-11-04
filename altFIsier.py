from mpu6050 import MPU6050
from time import sleep
# from vl53l0x import VL53L0X, Vl53l0xAccuracyMode
import board
import busio
import adafruit-circuitpython-vl53l0x

mpu = MPU6050()

mpu.Initialize()
sleep(0.1)
mpu.Calibrate()

i2c = busio.I2C(board.SCL, board.SDA)
tof = adafruit_vl53l0x(i2c)

while True:
    tof.range

# while True:
#     mpu.read()
#     print(mpu._angZ)