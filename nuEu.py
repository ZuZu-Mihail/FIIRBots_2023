import RPi.GPIO as GPIO
import time

right1 = 18
right2 = 12

left1 = 13
left2 = 19

START = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(left1, GPIO.OUT)
GPIO.setup(left2, GPIO.OUT)
GPIO.setup(right1, GPIO.OUT)
GPIO.setup(right2, GPIO.OUT)

GPIO.setup(START, GPIO.IN)

GPIO.output(left1,GPIO.LOW)
GPIO.output(left2,GPIO.LOW)
GPIO.output(right1,GPIO.LOW)
GPIO.output(right2,GPIO.LOW)

left1_pwm = GPIO.PWM(left1, 1000)
left2_pwm = GPIO.PWM(left2, 1000)
right1_pwm = GPIO.PWM(right1, 1000)
right2_pwm = GPIO.PWM(right2, 1000)

left1_pwm.start(0)
left2_pwm.start(0)
right1_pwm.start(0)
right2_pwm.start(0)

def ticks_ms():
    return time.time

#wait for reset
while GPIO.input(START) == 1:
    a = 0

#wait for start
while GPIO.input(START)  == 0:
    a = 0
print('START')

startTime = ticks_ms()

while (ticks_ms() - startTime <= 3) and GPIO.input(START) == 1:
    left1_pwm.start(0)
    left2_pwm.start(0.5)
    right1_pwm.start(0)
    right2_pwm.start(0.5)


left1_pwm.start(0)
left2_pwm.start(0)
right1_pwm.start(0)
right2_pwm.start(0)



