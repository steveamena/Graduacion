##This is the test code for the stepper motor
##Steve Mena Navarro PFG

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

motor1 = True
maxSpeed = 2667*2
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	if(motor1):
		Giro = 21
		Velocidad = 20
	else:
		Giro = 26
		Velocidad = 8
	GPIO.setup(Velocidad,GPIO.OUT)
	GPIO.setup(Giro,GPIO.OUT)
	#GPIO.setup(Velocidad2,GPIO.OUT)
	#GPIO.setup(Giro2,GPIO.OUT)	
#Set "el sentido de giro"
	#CW+: Sentido de giro
	GPIO.output(Giro,GPIO.LOW)
	#GPIO.output(Giro2,GPIO.LOW)
	#GPIO.output(21,GPIO.LOW)
	#CLK+: Velocidad del stepper
	stepper = GPIO.PWM(Velocidad,300)
	stepper.start(0)
	print("Motor Arrancado")
	stepper.ChangeDutyCycle(50)
	while True:
		stepper.ChangeDutyCycle(50)
		for i in range(10,maxSpeed,1):
			stepperSpeed(stepper,i)
			time.sleep(0.1)
		stepperSpeed(stepper,maxSpeed)
		time.sleep(5)
		
		for i in reversed(range(10,maxSpeed,1)):
			stepperSpeed(stepper,i)
			time.sleep(0.1)
		stepperSpeed(stepper,10)
		stepper.ChangeDutyCycle(0)
		time.sleep(5)
#		break
		

except(KeyboardInterrupt,SystemExit):
	stepper.stop()
	cleanAndExit()
finally:
	GPIO.cleanup()

