import RPi.GPIO as GPIO          
from time import sleep
from MPU6050 import MPU6050


mpu = MPU6050.mpu6050(0x68)
mpu.reset()
mpu.power_manage()
mpu.gyro_config()
mpu.accel_config()

in1 = 24
in2 = 23
en = 25
temp1=1

in3 = 17 # other motor
in4 = 27

en2 = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)


p=GPIO.PWM(en,1000)
p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("custom speed 0-10 (0-100%) & direction of motor is Forward & Backward.....")
print("\n")    


def forward():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)

    GPIO.output(in3,GPIO.HIGH) # other motor
    GPIO.output(in4,GPIO.LOW)

def backward():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)

    GPIO.output(in3,GPIO.LOW) # other motor
    GPIO.output(in4,GPIO.HIGH)

def stop():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)

    GPIO.output(in3,GPIO.LOW) # other motor
    GPIO.output(in4,GPIO.LOW)

def speed(x):
    p.ChangeDutyCycle(int(x)*10)



while True:

    gyroscope_data = mpu.read_gyroscope()
    accelerometer_data = mpu.read_accelerometer()

    print("Gyroscope data", gyroscope_data)


    # x=input()
    
    # if x=='r':
    #     print("run")
    #     if(temp1==1):
    #     #  GPIO.output(in1,GPIO.HIGH)
    #     #  GPIO.output(in2,GPIO.LOW)

    #     #  GPIO.output(in3,GPIO.HIGH) # other motor
    #     #  GPIO.output(in4,GPIO.LOW)
    #      forward()
    #      print("forward")
    #      x='z'
    #     else:
    #     #  GPIO.output(in1,GPIO.LOW)
    #     #  GPIO.output(in2,GPIO.HIGH)

    #     #  GPIO.output(in3,GPIO.LOW) # other motor
    #     #  GPIO.output(in4,GPIO.HIGH)
    #      backward()
    #      print("backward")
    #      x='z'


    # elif x=='s':
    #     print("stop")
    #     GPIO.output(in1,GPIO.LOW)
    #     GPIO.output(in2,GPIO.LOW)

    #     GPIO.output(in3,GPIO.LOW) # other motor
    #     GPIO.output(in4,GPIO.LOW)

    #     x='z'

    # elif x=='f':
    #     print("forward")
    #     # GPIO.output(in1,GPIO.HIGH)
    #     # GPIO.output(in2,GPIO.LOW)

    #     # GPIO.output(in3,GPIO.HIGH) # other motor
    #     # GPIO.output(in4,GPIO.LOW)
    #     forward()

    #     temp1=1
    #     x='z'

    # elif x=='b':
    #     print("backward")
    #     # GPIO.output(in1,GPIO.LOW)
    #     # GPIO.output(in2,GPIO.HIGH)

    #     # GPIO.output(in3,GPIO.LOW) # other motor
    #     # GPIO.output(in4,GPIO.HIGH)
    #     backward()

    #     temp1=0
    #     x='z'

    # elif x=='l':
    #     print("low")
    #     # p.ChangeDutyCycle(25)
    #     speed(2.5)
    #     x='z'

    # elif x=='m':
    #     print("medium")
    #     # p.ChangeDutyCycle(50)
    #     speed(5)
    #     x='z'

    # elif x=='h':
    #     print("high")
    #     # p.ChangeDutyCycle(75)
    #     speed(7.5)
    #     x='z'
     
    # elif x>=0 and x<=10:
    #     print("speed")
    #     # p.ChangeDutyCycle(int(x)*10)
    #     speed(x)
    #     x='z'
    #     break
    
    # elif x=='e':
    #     GPIO.cleanup()
    #     break


    
    # else:
    #     print("<<<  wrong data  >>>")
    #     print("please enter the defined data to continue.....")