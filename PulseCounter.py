from machine import Timer
from machine import Pin
from time import sleep

pulse_count = 0 # global variable
pulses_detected = False

pin_pulseDetection = Pin(26, mode=Pin.IN, pull=Pin.PULL_UP)

def pulse_detector(pin):
    global pulse_count
    pulse_count += 1

pin_pulseDetection.irq(trigger=Pin.IRQ_RISING,handler=pulse_detector)

def pulse_counter(timer):
    global pulses_detected
    global pulse_count
    if pulse_count > 5:
        pulses_detected = True
    else:
        pulses_detected = False 
    pulse_count = 0

soft_timer = Timer(mode=Timer.PERIODIC, period=10000, callback=pulse_counter)


while True:
        sleep(1)
        print(pulse_count)