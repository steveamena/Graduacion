##This is the test code for the stepper motor
##STeve Mena Navarro PFG
##Programa que funciona como probador de motor concentrado y steppers
##Tiene dos modos, uno para que funciones el concentrado y otro los steppers.

#Start importing the required libraries
import RPi.GPIO as GPIO
import time
import sys

#Define the function to clean up the GPIO
def cleanAndExit():
	print("Cleaning...")
	GPIO.cleanup()
	print("Bye...")
	sys.exit()

isStepper = False
maxSpeed 	= 2667*2
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	if(isStepper):
		Giro = 21
		Velocidad = 20
	else:
		Giro = 7
		Velocidad = 8
	GPIO.setup(Velocidad,GPIO.OUT)
	GPIO.setup(Giro,GPIO.OUT)

	#CW+: Sentido de giro
	#CLK+: Velocidad del stepper
	GPIO.output(Giro,GPIO.HIGH)
	
	stepper = GPIO.PWM(Velocidad,40)
	stepper.start(0)
	print("Motor Arrancado")
	stepper.ChangeDutyCycle(33)
	while True:
		"""for i in range(20,100,5):
			stepper.ChangeDutyCycle(i)
			time.sleep(0.5)
		i = 0
		for i in range(100,20,-5):
			stepper.ChangeDutyCycle(i)
			time.sleep(0.5)
		"""
		pass


except(KeyboardInterrupt,SystemExit):
	stepper.stop()
	cleanAndExit()
finally:
	GPIO.cleanup()
