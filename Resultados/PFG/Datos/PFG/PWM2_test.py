#Programa para probar motor de Concentrado y stepper al mismo tiempo.
#En ese momento el concentrado era controlado mediante un potenciometro.
#Este Script no se volvio a usar mas.
#Steve Mena Navarro PFG

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
	GPIO.output(ON,GPIO.LOW)
	#GPIO.output(Giro2,GPIO.LOW)
	#GPIO.output(21,GPIO.LOW)
	#CLK+: Velocidad del stepper
	GPIO.output(ON,GPIO.HIGH)
	
	stepper = GPIO.PWM(ON,120)
	pwm 	= GPIO.PWM(Velocidad,250)
	#stepper.start(0)
	pwm.start(0)
	print("Motor Arrancado")
	#stepper.ChangeDutyCycle(5)
	pwm.ChangeDutyCycle(0.1)
	while True:
		GPIO.output(ON,GPIO.HIGH)
		print "acelerando"
		for i in range(45,99,5):
			pwm.ChangeDutyCycle(i)
			time.sleep(0.25)
		GPIO.output(ON,GPIO.LOW)
		i = 0
		print "decelerando"
		GPIO.output(ON,GPIO.HIGH)
		for i in range(99,45,-5):
			pwm.ChangeDutyCycle(i)
			time.sleep(0.25)
		GPIO.output(ON,GPIO.LOW)
except(KeyboardInterrupt,SystemExit):
	stepper.stop()
	cleanAndExit()
finally:
	GPIO.cleanup()

