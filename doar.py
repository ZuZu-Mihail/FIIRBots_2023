from machine import Pin, I2C, PWM
from utime import sleep_ms, sleep_us, ticks_ms, ticks_diff
from vl53l0x import setup_tofl_device, TBOOT

# setup led
glb = Pin(22, Pin.OUT)
vrd = Pin(28, Pin.OUT)

# setup dc motor
dr = Pin(21, Pin.IN)
st = Pin(20, Pin.IN)

#KILL SWITCH START PIN
START = Pin(9, Pin.IN)

#LEDS
glb.value(1)
vrd.value(0)

# setup i2c bus 0
i2c_0 = I2C(id=0, sda=Pin(16), scl=Pin(17))

# setup bus 1
i2c_1 = I2C(id=1, sda=Pin(26), scl=Pin(27), freq=40000)

#PWM DC Mot
m_left1 = PWM(Pin(10))
m_left2 = PWM(Pin(11))

m_right1 = PWM(Pin(13))
m_right2 = PWM(Pin(12))

# set the PWM freq
PWM_FREQ = 1000

m_left1.freq(PWM_FREQ)
m_left2.freq(PWM_FREQ)
m_right1.freq(PWM_FREQ)
m_right2.freq(PWM_FREQ)

MOTOR_STATE = 'STOP'
MOTOR_MAX = 65025
MOTOR_SPEED = 0.4
REAL_SPEED = int(MOTOR_SPEED * MOTOR_MAX)

BRAKE_TIME = 350
BACK_TIME = 250
TURN_ANGLE = 80

sleep_us(TBOOT)

tofl0 = setup_tofl_device(i2c_0, 40000, 12, 8) 
tofl0.set_address(0x31)

sleep_us(TBOOT)

tofl1 = setup_tofl_device(i2c_0, 40000, 12, 8)
tofl1.set_address(0x32)

sleep_us(TBOOT)

tofl2 = setup_tofl_device(i2c_0, 40000, 12, 8)
tofl2.set_address(0x33)

#mark finished init
glb.value(0)
vrd.value(0)

#wait for reset
while START.value() == 1:
    a = 0

#wait for start
while START.value() == 0:
    a = 0

print('START')

first = 'RIGHT'

while True:


    while (START.value() == 0):
        m_left1.duty_u16(0)
        m_left2.duty_u16(0)
        m_right1.duty_u16(0)
        m_right2.duty_u16(0)
        #let the duty(0) take effect
        sleep_ms(1)
        m_left1.deinit()
        m_left2.deinit()
        m_right1.deinit()
        m_right2.deinit()
