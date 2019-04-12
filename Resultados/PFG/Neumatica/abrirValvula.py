#This is the file which opens and clses valves
#Steve Mena Navarro
#ITCR
#6 Marzo 2018

import RPi.GPIO as GPIO
import time

puerto=27
####
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(puerto,GPIO.OUT)
	while True:
		GPIO.output(puerto,1)
		print("1")
		time.sleep(2)
		GPIO.output(puerto,0)
		print("0")
		time.sleep(2)
finally:
	GPIO.cleanup()
	print("Bye")


