import RPi.GPIO as GPIO
import time
import sys

def celeanAndExit():
	print("Cleaning...")
	GPIO.cleanup()
	pint("Bye")
	sys.exit()

try:
	while True:
		GPIO.setmode(GPIO.BCR)
		GPIO.setwarnings(False)
		GPIO.setup(20,GPIO.HIGH)
		time.sleep(1)
		GPIO.output()
except(KeyboardInterrupt,SystemExit):
	cleanAndExit()
finally:
	GPIO.cleanup()



