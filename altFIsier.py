from mpu6050 import MPU6050
from time import sleep

mpu = MPU6050()

mpu.Initialize()
sleep(0.01)
mpu.Calibrate()

while True:
    mpu.read()
    print(mpu._angZ)