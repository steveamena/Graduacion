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

motor1 = True
valvula = 3

try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	if(motor1):
		Giro = 21
		Velocidad = 20
	else:
		Giro = 27
		Velocidad = 22
	GPIO.setup(Velocidad,GPIO.OUT)
	GPIO.setup(Giro,GPIO.OUT)
	GPIO.setup(valvula,GPIO.OUT)
	#GPIO.setup(Velocidad2,GPIO.OUT)
	#GPIO.setup(Giro2,GPIO.OUT)	
#Set "el sentido de giro"
	#CW+: Sentido de giro
	GPIO.output(Giro,0)
	GPIO.output(valvula,0)
	#GPIO.output(Giro2,GPIO.LOW)
	#GPIO.output(21,GPIO.LOW)
	#CLK+: Velocidad del stepper
	stepper = GPIO.PWM(Velocidad,600)
	stepper.start(0)
	print("Motor Arrancado")
	while True:
		stepper.ChangeDutyCycle(50)
		time.sleep(10)
		stepper.ChangeDutyCycle(0)
		time.sleep(0.5)
		for i in range(1,3):
			GPIO.output(valvula,GPIO.HIGH)
			time.sleep(1.5)
			GPIO.output(valvula,GPIO.LOW)
			time.sleep(1.5)
		break

except(KeyboardInterrupt,SystemExit):
	stepper.stop()
	cleanAndExit()
finally:
	GPIO.cleanup()

