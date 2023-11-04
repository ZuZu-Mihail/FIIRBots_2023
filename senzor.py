import RPi.GPIO as GPIO
from mpu6050 import MPU6050
from time import sleep

mpu = MPU6050()

mpu.Initialize()
sleep(0.1)
mpu.Calibrate()
print("b1")
Sumo = 0

in1 = 12
in2 = 32
in3 = 33
in4 = 35


# motoare sumo
# in1 = 24
# in2 = 23
# en = 25
# temp1=1

# in3 = 17 # other motor
# in4 = 27

# en2 = 22

# motoare maze 2 cu pi 0

# if Sumo == 0:
#     in1 = 18
#     # in1 = 12
#     in2 = 12
#     # in2 = 32
#     # en = 22
#     temp1=1

#     in3 = 13 # other motor
#     # in3 = 33 # other motor
#     # in4 = 35
#     in4 = 19

# elif Sumo == 1:
#     in1 = 24
#     in2 = 23
#     en = 25
#     temp1=1

#     in3 = 17 # other motor
#     in4 = 27

#     en2 = 22

# en2 = 25

START = 40

# GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
# GPIO.setup(en,GPIO.OUT)

print("b2")


GPIO.setup(START, GPIO.IN)

# if Sumo == 1:
#     GPIO.setup(en,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

print("b3")


# GPIO.setup(in3,GPIO.OUT)
# GPIO.setup(in4,GPIO.OUT)
# GPIO.setup(en2,GPIO.OUT)
# if Sumo == 1:
#     GPIO.setup(en2,GPIO.OUT)
# GPIO.output(in3,GPIO.LOW)
# GPIO.output(in4,GPIO.LOW)

pi1_pwm = GPIO.PWM(in1, 1000)
pi2_pwm = GPIO.PWM(in2, 1000)
pi3_pwm = GPIO.PWM(in3, 1000)
pi4_pwm = GPIO.PWM(in4, 1000)

pi1_pwm.start(0)
pi2_pwm.start(0)
pi3_pwm.start(0)
pi4_pwm.start(0)

# speed = 0
print("b4")

def PWM_Setup(x):
    global speed
    aux = int(speed)
    print(aux)
    if x > 0: # forward
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)

        GPIO.output(in3,GPIO.HIGH) # other motor
        GPIO.output(in4,GPIO.LOW)

        if Sumo == 0:
            pi1_pwm.ChangeDutyCycle(aux)
            pi2_pwm.ChangeDutyCycle(0)
            pi3_pwm.ChangeDutyCycle(aux)
            pi4_pwm.ChangeDutyCycle(0)

    elif x < 0: # backward
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW) # other motor
        GPIO.output(in4,GPIO.HIGH)

        if Sumo == 0:
            pi1_pwm.ChangeDutyCycle(0)
            pi2_pwm.ChangeDutyCycle(aux)
            pi3_pwm.ChangeDutyCycle(0)
            pi4_pwm.ChangeDutyCycle(aux)



    else: # stop

        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW) # other motor
        GPIO.output(in4,GPIO.LOW)

        if Sumo == 0:
            pi1_pwm.ChangeDutyCycle(0)
            pi2_pwm.ChangeDutyCycle(0)
            pi3_pwm.ChangeDutyCycle(0)
            pi4_pwm.ChangeDutyCycle(0)



# # p=GPIO.PWM(en,1000)
# # p.start(25)

# if Sumo == 1:
#     p1=GPIO.PWM(en,1000)
#     p1.start(25)
#     p2=GPIO.PWM(en2,1000)
#     p2.start(25)


# print("\n")
# print("The default speed & direction of motor is LOW & Forward.....")
# print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
# print("custom speed 0-10 (0-100%) & direction of motor is Forward & Backward.....")
# print("\n")    


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

#     if Sumo == 1:
#         p1.ChangeDutyCycle(int(x)*10)
#         p2.ChangeDutyCycle(int(x)*10)

print("1")
#wait for reset
while GPIO.input(START) == 1:
    a = 0

print("1")
#wait for start
while GPIO.input(START)  == 0:
    a = 0

print('START')


print("haidaa")
while True:
    print(GPIO.input(START))
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    print("b1")

    while GPIO.input(START) == 1:
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)

        GPIO.output(in3,GPIO.HIGH) # other motor
        GPIO.output(in4,GPIO.LOW)

        pi1_pwm.ChangeDutyCycle(75)
        pi2_pwm.ChangeDutyCycle(0)
        pi3_pwm.ChangeDutyCycle(75)
        pi4_pwm.ChangeDutyCycle(0)
    else:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        pi1_pwm.ChangeDutyCycle(0)
        pi2_pwm.ChangeDutyCycle(0)
        pi3_pwm.ChangeDutyCycle(0)
        pi4_pwm.ChangeDutyCycle(0)
    # while (GPIO.input(START)  == 0):
    #     stop()

    # if (GPIO.input(START) == 0):
    #     stop
    # else:
    #     mpu.read()
    #     print(mpu._angZ)
        
    #     speedy(0.1)
    #     forward()
    #     sleep(0.1)

    # x=input()
    
    # if x=='r':
    #     print("run")
    #     if(temp1==1):
    #      forward()
    #      print("forward")
    #      x='z'
    #     else:
    #      backward()
    #      print("backward")
    #      x='z'

    # elif x=='s':
    #     print("stop")
    #     stop()

    #     x='z'

    # elif x=='f':
    #     print("forward")

    #     forward()

    #     temp1=1
    #     x='z'

    # elif x=='b':
    #     print("backward")

    #     backward()

    #     temp1=0
    #     x='z'

    # elif x=='l':
    #     print("low")
    #     speedy(2.5)
    #     x='z'

    # elif x=='m':
    #     print("medium")
    #     speedy(5)
    #     x='z'

    # elif x=='h':
    #     print("high")
    #     speedy(7.5)
    #     x='z'
    # elif x=='full': 
    #     print("full")
    #     speedy(10)
    #     x='z'


    # elif x=='e':
    #     GPIO.cleanup()
    #     break


    
    # else:
    #     print("<<<  wrong data  >>>")
    #     print("please enter the defined data to continue.....")