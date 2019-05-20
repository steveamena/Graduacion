##Codigo para probar el funcionamiento de los steppers
##Steve Mena Navarro PFG
##15/5/2019
##GC@2019


"""		LEEME:
	Para probar los motores escribir True si necesita probar el
	Mineral, en caso contrario se probara la levadura.
	Si desea probar con diferentes velocidades colocar aceleracion en True
	-------------------------------
	Para los steppers se cumple:
		CW+		:Sentido de giro.
		CLK+	:Velocidad de giro.
		"""
#Importar las libreria requeridas		
import RPi.GPIO as GPIO
import time
import sys

#Definir la funciona para limpiar el GPIO
def cleanAndExit():
	print("Cleaning...")
	GPIO.cleanup()
	print("Bye...")
	sys.exit()

def stepperSpeed(stepper,speed):
	stepper.ChangeFrequency(speed)

mineral 	= True
maxSpeed 	= 2667
aceleracion	= True

try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	if(mineral):
		Giro 		= 21
		Velocidad 	= 20
		motor		= "Mineral"
	else:
		Giro 		= 26
		Velocidad 	= 25
		motor		= "Levadura"
		
	GPIO.setup(Velocidad,GPIO.OUT)
	GPIO.setup(Giro,GPIO.OUT)
	stepper = GPIO.PWM(Velocidad,300)
	stepper.start(0)
	print(motor," arrancado")
	c = 0
	
	while True:
		stepper.ChangeDutyCycle(50)
		if aceleracion:
			for i in range(10,maxSpeed,10):
				stepperSpeed(stepper,i)
				time.sleep(0.1)
			
			for i in reversed(range(10,maxSpeed,10)):
				stepperSpeed(stepper,i)
				time.sleep(0.1)

		else:
			if (c==0):
				stepperSpeed(stepper,maxSpeed/2)
				c += 0
	#break
		

except(KeyboardInterrupt,SystemExit):
	stepper.stop()
	cleanAndExit()
finally:
	GPIO.cleanup()

