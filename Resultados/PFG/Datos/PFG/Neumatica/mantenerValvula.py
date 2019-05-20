#This is the file which opens and clse the gates
#Steve Mena Navarro
#ITCR
#4 September 2018

import RPi.GPIO as GPIO
import time

puerto=2
####
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(puerto,GPIO.OUT)
	while True:
		GPIO.output(puerto,0)
		time.sleep(20)
		GPIO.output(puerto,1)
		print("1")
		time.sleep(20)
		GPIO.output(puerto,0)
		print("0")
		break
		#time.sleep(2)
finally:
	GPIO.cleanup()
	print("Bye")


