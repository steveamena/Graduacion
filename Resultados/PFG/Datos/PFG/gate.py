#Archivo para probar PWM a diferentes ciclos de trabajo.
#Steve Mena Navarro
#ITCR
#4 September 2018

import RPi.GPIO as GPIO
import time

####
try:
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(11,GPIO.OUT)
	pwm = GPIO.PWM(11,50)
	pwm.start(6.8);
	time.sleep(1);
	pwm.ChangeDutyCycle(4.5);
	time.sleep(1)
	pwm.ChangeDutyCycle(6.8);
	time.sleep(2)
	pwm.ChangeDutyCycle(5);

finally:
	GPIO.cleanup()
	print("Bye")


