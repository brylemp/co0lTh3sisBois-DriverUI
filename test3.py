import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

while 1:
	uid,idnum = reader.read_no_block()
	print(uid)
	print(idnum)

GPIO.cleanup()

