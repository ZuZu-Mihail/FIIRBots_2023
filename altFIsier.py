from mpu6050 import MPU6050
from time import sleep

mpu = MPU6050()

mpu.Initialize()

mpu.Calibrate()

i = 0

while True:
    mpu.read()
    print(mpu._angZ)
    sleep(0.005)
    