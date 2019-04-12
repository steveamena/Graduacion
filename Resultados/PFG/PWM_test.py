##This is the test code for the stepper motor
##STeve Mena Navarro PFG

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

def stepperSpeed(stepper,speed):
	stepper.ChangeFrequency(speed)

motor1 = False
maxSpeed = 2667*2
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	if(motor1):
		Giro = 21
		Velocidad = 20
	else:
		ON = 7
		Velocidad = 8
	GPIO.setup(Velocidad,GPIO.OUT)
	GPIO.setup(ON,GPIO.OUT)
	#GPIO.setup(Velocidad2,GPIO.OUT)
	#GPIO.setup(Giro2,GPIO.OUT)	
#Set "el sentido de giro"
	#CW+: Sentido de giro
	GPIO.output(ON,GPIO.HIGH)
	#GPIO.output(Giro2,GPIO.LOW)
	#GPIO.output(21,GPIO.LOW)
	#CLK+: Velocidad del stepper
	stepper = GPIO.PWM(Velocidad,40)
	stepper.start(0)
	print("Motor Arrancado")
	stepper.ChangeDutyCycle(95)
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

