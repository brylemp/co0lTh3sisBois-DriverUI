import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)
x = 0 

def button_callback(channel):
	global x
	x = x+1
	print(x)

GPIO.add_event_detect(16,GPIO.RISING,callback=button_callback)


while 1:
	pass
	
GPIO.cleanup()
		
 
 
