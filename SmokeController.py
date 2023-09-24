from machine import Timer
from machine import Pin
from time import sleep
import random

pulse_count = 0
motionDetected = False
smokeMachineReady = False

def motion_detector(pin):
    global motionDetected
    motionDetected = True

pin_sensor = Pin(16, mode=Pin.IN, pull=Pin.PULL_DOWN)
pin_sensor.irq(trigger=Pin.IRQ_RISING,handler=motion_detector)

pin_ActivateSmoke = Pin(28, Pin.OUT)

def pulse_detector(pin):
    global pulse_count
    pulse_count += 1

def pulse_counter(timer):
    global smokeMachineReady
    global pulse_count
    if pulse_count > 20:
        smokeMachineReady = True
    else:
        smokeMachineReady = False 
    pulse_count = 0

pin_pulseDetection = Pin(26, mode=Pin.IN, pull=Pin.PULL_UP)
pin_pulseDetection.irq(trigger=Pin.IRQ_RISING,handler=pulse_detector)

pulse_timer = Timer(mode=Timer.PERIODIC, period=1000, callback=pulse_counter)

while True:
        if smokeMachineReady and motionDetected:
             pin_ActivateSmoke.value(1)
             activeDelay = random.randrange(2,6)
             sleep(activeDelay)
             pin_ActivateSmoke.value(0)
             sleepDelay = random.randrange(20,40)
             sleep(sleepDelay)
             motionDetected = False
