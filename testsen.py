
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)    #beam sensor 1
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #beam sensor 2

try:
	while(True):
		print(not GPIO.input(5))
		print(not GPIO.input(26))
except KeyboardInterrupt:
	GPIO.cleanup()

import time
 
import board
import digitalio
 
 
