from mpu6050 import MPU6050
from time import sleep
import time

mpu = MPU6050()

mpu.Initialize()

mpu.Calibrate()

i = 0

print(time.tick_ms())

def ticks_ms():
    return int(time.time() * 1000)

while True:
    print(ticks_ms())

# while True:
#     mpu.read()
#     print(mpu._angZ)
#     sleep(0.005)
    