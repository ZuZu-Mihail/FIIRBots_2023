from mpu6050 import MPU6050
from time import sleep
import VL53L0X

# Create a VL53L0X object
tof = VL53L0X.VL53L0X()

# Start ranging
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

print(tof.get_distance())

mpu = MPU6050()

mpu.Initialize()
sleep(0.1)
mpu.Calibrate()




# while True:
#     mpu.read()
#     print(mpu._angZ)