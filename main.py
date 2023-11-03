import RPi.GPIO as GPIO          
from time import sleep
# motoare sumo
# in1 = 24
# in2 = 23
# en = 25
# temp1=1

# in3 = 17 # other motor
# in4 = 27

# en2 = 22

# motoare maze 2 cu pi 0

in1 = 1
in2 = 26
# en = 22
temp1=1

in3 = 23 # other motor
in4 = 24

# en2 = 25


GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
# GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
# GPIO.setup(en2,GPIO.OUT)
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
        pi1_pwm.ChangeDutyCycle(aux)
        pi2_pwm.ChangeDutyCycle(0)
        pi3_pwm.ChangeDutyCycle(aux)
        pi4_pwm.ChangeDutyCycle(0)
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)

        GPIO.output(in3,GPIO.HIGH) # other motor
        GPIO.output(in4,GPIO.LOW)


    elif x < 0: # backward
        pi1_pwm.ChangeDutyCycle(0)
        pi2_pwm.ChangeDutyCycle(aux)
        pi3_pwm.ChangeDutyCycle(0)
        pi4_pwm.ChangeDutyCycle(aux)

        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW) # other motor
        GPIO.output(in4,GPIO.HIGH)


    else: # stop
        pi1_pwm.ChangeDutyCycle(0)
        pi2_pwm.ChangeDutyCycle(0)
        pi3_pwm.ChangeDutyCycle(0)
        pi4_pwm.ChangeDutyCycle(0)

        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW) # other motor
        GPIO.output(in4,GPIO.LOW)
        


# p=GPIO.PWM(en,1000)
# p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("custom speed 0-10 (0-100%) & direction of motor is Forward & Backward.....")
print("\n")    


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



while True:


    x=input()
    
    if x=='r':
        print("run")
        if(temp1==1):
        #  GPIO.output(in1,GPIO.HIGH)
        #  GPIO.output(in2,GPIO.LOW)

        #  GPIO.output(in3,GPIO.HIGH) # other motor
        #  GPIO.output(in4,GPIO.LOW)
         forward()
         print("forward")
         x='z'
        else:
        #  GPIO.output(in1,GPIO.LOW)
        #  GPIO.output(in2,GPIO.HIGH)

        #  GPIO.output(in3,GPIO.LOW) # other motor
        #  GPIO.output(in4,GPIO.HIGH)
         backward()
         print("backward")
         x='z'

    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)

        GPIO.output(in3,GPIO.LOW) # other motor
        GPIO.output(in4,GPIO.LOW)

        x='z'

    elif x=='f':
        print("forward")
        # GPIO.output(in1,GPIO.HIGH)
        # GPIO.output(in2,GPIO.LOW)

        # GPIO.output(in3,GPIO.HIGH) # other motor
        # GPIO.output(in4,GPIO.LOW)
        forward()

        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        # GPIO.output(in1,GPIO.LOW)
        # GPIO.output(in2,GPIO.HIGH)

        # GPIO.output(in3,GPIO.LOW) # other motor
        # GPIO.output(in4,GPIO.HIGH)
        backward()

        temp1=0
        x='z'

    elif x=='l':
        print("low")
        # p.ChangeDutyCycle(25)
        speedy(2.5)
        x='z'

    elif x=='m':
        print("medium")
        # p.ChangeDutyCycle(50)
        speedy(5)
        x='z'

    elif x=='h':
        print("high")
        # p.ChangeDutyCycle(75)
        speedy(7.5)
        x='z'
    elif x=='full':
        print("full")
        # p.ChangeDutyCycle(100)
        speedy(10)
        x='z'


    elif x=='e':
        GPIO.cleanup()
        break


    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")