import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

while 1:
	time.sleep(100)
	uid,idnum = reader.read_no_block()
	print(uid)
	print(idnum)

GPIO.cleanup()

