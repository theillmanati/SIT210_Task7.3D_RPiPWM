#!/usr/bin/python
 
# LIBRARIES #
import RPi.GPIO as GPIO
import time
from gpiozero import PWMLED
 
# CONSTANTS #
SPEED_OF_SOUND = 34000 # Speed of sund is 34000 cm/s.
MAX_DISTANCE = 30 # Sensor data monitored by LED within 30 cm so demonstration can be easily shot
 
# HARDWARE #
GPIO.setmode(GPIO.BCM)
TRIGGER = 23 # Trig pin of ultrasonic sensor connected to GPIO pin 23 (pin 16)
ECHO = 24 # Echo pin of ultrasonic sensor connected to GPIO pin 24 (pin 18)
LED = PWMLED(18) # Anode of blue LED connected to GPIO pin 18 (pin 12)
 
GPIO.setup(TRIGGER, GPIO.OUT) # Trig pin of ultrasonic sensor will be sending output
GPIO.setup(ECHO, GPIO.IN) # Echo pin of ultrasonic sensor will be getting input
 
# FUNCTIONS #
def distance():
    GPIO.output(TRIGGER, True) # Set trigger to HIGH
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False) # After 0.1 ms, set trigger to LOW
     
    while GPIO.input(ECHO) == 0:
        startTime = time.time() # Time of start of pulse saved
        
    while GPIO.input(ECHO) == 1:
        stopTime = time.time() # Time of pulse arriving to echo sensor saved
         
    timeElapsed = stopTime - startTime # time taken for pulse from trig to reach echo
    distance = timeElapsed * SPEED_OF_SOUND / 2 #time elapsed is multiplied by speed of sound, and divided by 2, as the pulse goes back and forth

    return distance

try:
    while True:
        currentDistance = distance()
        print ("Measured distance = %.2f cm" % currentDistance) # Current distance from ultrasonic sensor printed to 2 sig figs with units
        
        if currentDistance > MAX_DISTANCE:
            LED.value = 0 # If beyond maximum distance LED will be off
            
        if currentDistance <= MAX_DISTANCE:
            proximity = 1 - (currentDistance / MAX_DISTANCE)
            LED.value = proximity # If below max distance the LED will be turned on to some degree of its brightness, which will change depending how close it is
            
        time.sleep(1) # Updates every 1 s
        
except keyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
