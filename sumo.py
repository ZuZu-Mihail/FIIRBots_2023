import RPi.GPIO as GPIO
from mpu6050 import MPU6050
from time import sleep

mpu = MPU6050()

mpu.Initialize()
sleep(0.1)
mpu.Calibrate()


Sumo_EN = 0

GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

ML2_RIGHT_PIN = 7

GPIO.setup(ML2_RIGHT_PIN, GPIO.IN)

def read_ml2():
    right_sensor = GPIO.input(ML2_RIGHT_PIN)
    return right_sensor


# motoare Sumo_EN
# in1 = 24
# in2 = 23
# en = 25
# temp1=1

# in3 = 17 # other motor
# in4 = 27

# en2 = 22

# motoare maze 2 cu pi 0

if Sumo_EN == 0:
    in1 = 33
    in2 = 35
    # en = 22
    temp1=1

    in3 = 10 # other motor
    in4 = 32

elif Sumo_EN == 1:
    in1 = 24
    in2 = 23
    en = 25
    temp1=1

    in3 = 17 # other motor
    in4 = 27

    en2 = 22

# en2 = 25


GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
# GPIO.setup(en,GPIO.OUT)
if Sumo_EN == 1:
    GPIO.setup(en,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
# GPIO.setup(en2,GPIO.OUT)
if Sumo_EN == 1:
    GPIO.setup(en2,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

pi1_pwm = GPIO.PWM(in1, 1000)
pi2_pwm = GPIO.PWM(in2, 1000)
pi3_pwm = GPIO.PWM(in3, 1000)
pi4_pwm = GPIO.PWM(in4, 1000)

pi1_pwm.start(0)
pi2_pwm.start(0)
pi3_pwm.start(0)
pi4_pwm.start(0)

speed = 0

def PWM_Setup(x):
    global speed
    aux = int(speed)
    print(aux)
    if x > 0: # forward
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)

        GPIO.output(in3,GPIO.HIGH) # other motor
        GPIO.output(in4,GPIO.LOW)

        if Sumo_EN == 0:
            pi1_pwm.ChangeDutyCycle(aux)
            pi2_pwm.ChangeDutyCycle(0)
            pi3_pwm.ChangeDutyCycle(aux)
            pi4_pwm.ChangeDutyCycle(0)

    elif x < 0: # backward
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW) # other motor
        GPIO.output(in4,GPIO.HIGH)

        if Sumo_EN == 0:
            pi1_pwm.ChangeDutyCycle(0)
            pi2_pwm.ChangeDutyCycle(aux)
            pi3_pwm.ChangeDutyCycle(0)
            pi4_pwm.ChangeDutyCycle(aux)



    else: # stop

        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW) # other motor
        GPIO.output(in4,GPIO.LOW)

        if Sumo_EN == 0:
            pi1_pwm.ChangeDutyCycle(0)
            pi2_pwm.ChangeDutyCycle(0)
            pi3_pwm.ChangeDutyCycle(0)
            pi4_pwm.ChangeDutyCycle(0)
 

if Sumo_EN == 1:
    p1=GPIO.PWM(en,1000)
    p1.start(25)
    p2=GPIO.PWM(en2,1000)
    p2.start(25)

def forward():
    # GPIO.output(in1,GPIO.HIGH)
    # GPIO.output(in2,GPIO.LOW)

    # GPIO.output(in3,GPIO.HIGH) # other motor
    # GPIO.output(in4,GPIO.LOW)
    PWM_Setup(1)

def backward():
    # GPIO.output(in1,GPIO.LOW)
    # GPIO.output(in2,GPIO.HIGH)

    # GPIO.output(in3,GPIO.LOW) # other motor
    # GPIO.output(in4,GPIO.HIGH)
    PWM_Setup(-1)

def stop():
    # GPIO.output(in1,GPIO.LOW)
    # GPIO.output(in2,GPIO.LOW)

    # GPIO.output(in3,GPIO.LOW) # other motor
    # GPIO.output(in4,GPIO.LOW)
    PWM_Setup(0)

def speedy(x):
    # p.ChangeDutyCycle(int(x)*10)
    global speed
    speed = int(x) * 10

    if Sumo_EN == 1:
        p1.ChangeDutyCycle(int(x)*10)
        p2.ChangeDutyCycle(int(x)*10)

def rotire(degrees):
    while mpu.read() < degrees:
        speedy(10)
        forward()

# diamtru terenului: 122 cm
# raza terenului: 61 cm
# 20 x 20 cm robot
# max_counts = 122 / 20 = 6.1

MAX_COUNTS = 10

while True:
    mpu.read()
    print(mpu._angZ)

    x=input()

    right_sensor = read_ml2()
    print(f"Right sensor: {right_sensor}")

    # count = 0

    # if right_sensor == 0:
    #     speedy(10)
    #     forward()
    # elif count < MAX_COUNTS :
    #     count += 1
    #     rotire(178)
    # elif count == MAX_COUNTS:
    #     count = 0
    # elif count < MAX_COUNTS * 2:
    #     rotire(-178)
    # elif count == MAX_COUNTS * 2:
    #     count = 0


    # speedy(10)
    # forward()
    
    # # senzor distanta < 30
    # if right_sensor:
        

    if x=='r':
        print("run")
        if(temp1==1):
         forward()
         print("forward")
         x='z'
        else:
         backward()
         print("backward")
         x='z'

    elif x=='s':
        print("stop")
        stop()

        x='z'

    elif x=='f':
        print("forward")

        forward()

        temp1=1
        x='z'

    elif x=='b':
        print("backward")

        backward()

        temp1=0
        x='z'

    elif x=='l':
        print("low")
        speedy(2.5)
        x='z'

    elif x=='m':
        print("medium")
        speedy(5)
        x='z'

    elif x=='h':
        print("high")
        speedy(7.5)
        x='z'
    elif x=='full': 
        print("full")
        speedy(10)
        x='z'


    elif x=='e':
        GPIO.cleanup()
        break


    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")