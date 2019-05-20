##Codigo para probar el funcionamiento del concentrado
##Steve Mena Navarro PFG
##15/5/2019
##GC@2019


"""		LEEME:
	Programa para probar los otros dos motores Concentrado y Citrocom.
	Si desea probar el concentrado:
		colocar concentrado en True
	Si desea probar con diferentes velocidades:
		colocar aceleracion en True
	-------------------------------
	El concentrado debe conectarse como:
		Enceder		:GPIO7
		Velocidad	:GPIO8
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

maxSpeed 	= 99
aceleracion	= True
concentrado = True

if concentrado:
	encendido	= 7
	velocidad	= 8
	motor		= "Concentrado"
	
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	
	#Inicializar puertos del motor
	GPIO.setup(encendido,GPIO.OUT)
	GPIO.setup(velocidad,GPIO.OUT)	
	
	#Colocar todas salidas en bajo
	GPIO.output(encendido,0)
	GPIO.output(velocidad,0)

	#Configurar PWM del concentrado
	ConPWM	= GPIO.PWM(velocidad,250)

	#Encendido motor Concentrado
	velocidad = 99
	ConPWM.ChangeDutyCycle(velocidad)
	print(motor," arrancado")
	GPIO.output(encendido,GPIO.HIGH)
	
	c = 0
	ConPWM.start(0)
	
	while True:
		if aceleracion:
			for i in range(10,maxSpeed,1):
				ConPWM.ChangeDutyCycle(i)
				time.sleep(0.1)
			for i in reversed(range(10,maxSpeed,1)):
				ConPWM.ChangeDutyCycle(i)
				time.sleep(0.1)

		else:
			if (c==0):
				ConPWM.ChangeDutyCycle(maxSpeed)
				c += 0
	#break
		

except(KeyboardInterrupt,SystemExit):
	ConPWM.stop()
	GPIO.output(encendido,GPIO.LOW)
	cleanAndExit()
	
finally:
	GPIO.cleanup()
	print("Bye")
