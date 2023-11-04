from mpu6050 import MPU6050
from time import sleep
from vl53l0x import VL53L0X, Vl53l0xAccuracyMode

mpu = MPU6050()

mpu.Initialize()
sleep(0.1)
mpu.Calibrate()

tof = VL53L0X()

tof.open()

tof.start_ranging(Vl53l0xAccuracyMode.GOOD)

while True:
    distance = tof.get_distance()
    print(distance)

# while True:
#     mpu.read()
#     print(mpu._angZ)