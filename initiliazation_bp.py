import RPi.GPIO as GPIO
import time
import os
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)   #bailout button


global loop
loop=True

global go_in_to
go_in_to=False

def GPIO22_callback(channel):
	if GPIO.input(27):
		print('go into call back')
		global go_in_to
		go_in_to=True
		print('go',go_in_to)
		GPIO.cleanup()
		os.system('sudo python BeeCam_NN.py')
		print('bakc from call back')
		go_in_to=False
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(27, GPIO.IN)   #bailout button
		GPIO.add_event_detect(27, GPIO.BOTH, callback=GPIO22_callback, bouncetime=300)
		
GPIO.add_event_detect(27, GPIO.BOTH, callback=GPIO22_callback, bouncetime=300)

try:
	while (loop):
		if(not go_in_to):
			print('go',go_in_to)
		#print(loop)
		time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
