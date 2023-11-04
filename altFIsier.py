from mpu6050 import MPU6050
from time import sleep
# from vl53l0x import VL53L0X, Vl53l0xAccuracyMode

mpu = MPU6050()

mpu.Initialize()
sleep(0.1)
mpu.Calibrate()



# while True:
#     mpu.read()
#     print(mpu._angZ)