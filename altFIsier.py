from mpu6050 import MPU6050
from time import sleep
import time

mpu = MPU6050()

mpu.Initialize()

mpu.Calibrate()

while True:
    mpu.read()
    print(mpu._angZ)