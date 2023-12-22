import RPi.GPIO as GPIO
import time
import os

os.system('raspi-gpio set 19 ip')
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)

def turnOnScreen():
    os.system('raspi-gpio set 19 op a5')
    GPIO.output(18, GPIO.HIGH)

def turnOffScreen():
    os.system('raspi-gpio set 19 ip')
    GPIO.output(18, GPIO.LOW)

def shutdown():
    os.system("sudo shutdown -h now")

turnOffScreen()
screen_on = False
screen_turned_on_once = False
screen_off_time = 0
screen_on_time = 0 
tap_count = 0

while True:
    input_state = not GPIO.input(26)

    if input_state != screen_on:
        screen_on = input_state
        if screen_on:
            turnOnScreen()
            screen_turned_on_once = True
            screen_on_time += 0.3
        else:
            turnOffScreen()
            screen_on_time = 0
        
    if screen_on and screen_off_time >0:
        screen_off_time = 0
        tap_count += 1
        
    if screen_on and screen_on_time >= 5:
            screen_on_time = 0
            tap_count = 1

    if screen_turned_on_once and not screen_on:
        screen_off_time += 0.3
        if screen_off_time >= 30:
            shutdown()

    if tap_count >= 2 and screen_off_time >= 10:
        shutdown()

    time.sleep(0.3)
