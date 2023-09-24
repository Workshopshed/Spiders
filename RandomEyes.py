from time import sleep, sleep_ms
from machine import Pin
from time import ticks_add, ticks_diff, ticks_ms
import random

outDelay = [0,0,0,0,0]
outPins = [Pin(27, Pin.OUT),Pin(26, Pin.OUT),Pin(22, Pin.OUT), Pin(21, Pin.OUT),Pin(20, Pin.OUT)]
motionDetected = False
effectOnDelay = 0
effectOffTime = 0
effectRunning = False

#Test outputs
for i in range(0, 4):
    outPins[i].value(1)
    sleep_ms(500)
for i in range(0, 4):
    outPins[i].value(0)
    sleep_ms(500)

pin_sensor = Pin(16, mode=Pin.IN, pull=Pin.PULL_DOWN)

def motion_detector(pin):
    global motionDetected
    motionDetected = True

pin_sensor.irq(trigger=Pin.IRQ_RISING,handler=motion_detector)

def runEffect():
    global outDelay, outPins
    if random.random() < 0.6: 
        nextOutput = random.randrange(4)

        if outDelay[nextOutput] == 0:
            nextDelay = random.randrange(3000) # 3000ms
            outDelay[nextOutput] = ticks_add(ticks_ms(),nextDelay)
            outPins[nextOutput].value(1)

    for i in range(0, 4):
        if outDelay[i] != 0:
            if ticks_diff(ticks_ms(), outDelay[i]) > 0: # Delay over reset
                outDelay[i] = 0
                outPins[i].value(0)

    sleep(1)

#Main Loop
while True:
    if not effectRunning and motionDetected:
        effectOnDelay = random.randrange(30000)
        effectOffTime = ticks_add(ticks_ms(),effectOnDelay)
        effectRunning = True

    if ticks_diff(ticks_ms(), effectOffTime) > 0:
        motionDetected = False
        effectRunning = False
        for i in range(0, 4):
            outPins[i].value(0)

    if effectRunning:
        runEffect()



