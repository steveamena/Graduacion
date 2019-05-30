##Codigo para probar ambos motores steppers al mismo tiempo.
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
	stepper.ChangeFrequency(speed/3)

motor1 = False
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	#if(motor1):
	Giro1 = 21
	Velocidad1 = 20
	#else:
	Giro2 = 22
	Velocidad2 = 27
	GPIO.setup(Velocidad1,GPIO.OUT)
	GPIO.setup(Giro1,GPIO.OUT)
	GPIO.setup(Velocidad2,GPIO.OUT)
	GPIO.setup(Giro2,GPIO.OUT)	
#Set "el sentido de giro"
	#CW+: Sentido de giro
	GPIO.output(Giro1,GPIO.LOW)
	GPIO.output(Giro2,GPIO.LOW)
	#GPIO.output(21,GPIO.LOW)
	#CLK+: Velocidad del stepper
	stepper = GPIO.PWM(Velocidad1,300)
	stepper2 = GPIO.PWM(Velocidad2,300)
	stepper.start(0)
	stepper2.start(0)
	stepper.ChangeDutyCycle(50)
	stepper2.ChangeDutyCycle(50)
	while True:
		for i in range(10,600,6):
			stepperSpeed(stepper,i)
			time.sleep(0.01)
		for i in reversed(range(10,600,6)):
			stepperSpeed(stepper,i)
			time.sleep(0.01)
#		break

except(KeyboardInterrupt,SystemExit):
	stepper.stop()
	cleanAndExit()
finally:
	GPIO.cleanup()

