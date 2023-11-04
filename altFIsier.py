from mpu6050 import MPU6050
from time import sleep
# from vl53l0x import VL53L0X, Vl53l0xAccuracyMode
import vl53l0x

mpu = MPU6050()

mpu.Initialize()
sleep(0.1)
mpu.Calibrate()

print("declare")
tof = vl53l0x.VL53L0X()

print("open")
tof.open()

print("range")
tof.start_ranging(vl53l0x.Vl53l0xAccuracyMode.GOOD)

while True:
    distance = tof.get_distance()
    print(distance)

# while True:
#     mpu.read()
#     print(mpu._angZ)