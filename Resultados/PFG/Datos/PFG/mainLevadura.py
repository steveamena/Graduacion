
##This is the test code for the stepper motor
##STeve Mena Navarro PFG

#Start importing the required libraries
import RPi.GPIO as GPIO
import time
import sys
##Importar las librerias para la celda de carga
from hx711 import HX711

#funcion para inicializar la celda de carga.
def startLoadCell(sensibilidad):
	hx = HX711(5,6,'A')
	hx.set_reading_format("LSB","MSB") 	#Configura el modo de lectura
	hx.set_reference_unit(sensibilidad)
	hx.reset()
	hx.tare()
	return hx

#Define la funcion para limpiar el GPIO
def cleanAndExit():
	print("Cleaning...")
	GPIO.cleanup()
	print("Bye...")
	sys.exit()

##Funcion para cambiar la velocidad del motor a pasos
def stepperSpeed(stepper,speed):
	stepper.ChangeFrequency(speed*3)

##Inicia el codigo main
#Inicializar el GPIO
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(27,GPIO.OUT)
	GPIO.setup(22,GPIO.OUT)

	#Configura "el sentido de giro"
	GPIO.output(27,GPIO.LOW)
	#GPIO.output(21,GPIO.LOW)
	stepper = GPIO.PWM(22,300)
	stepper.start(0)
	masaObjetivo = 100 	#Variable que almacena la masa objetivo
	print("Motor arrancado...")
	#Obtener la primera medicion de la masa
	hx = startLoadCell(11734.0)
	masa = hx.get_weight()
	print("Celda de carga arrancada...")
##While que arranca el motor mientras haga falta masa	
	condicion = True
	while True:
#		stepperSpeed(stepper,60)
		if(masa/masaObjetivo<0.75):
			stepper.ChangeFrequency(700)
			stepper.ChangeDutyCycle(50)
		else:
			if(masa/masaObjetivo>=1):
				stepper.ChangeFrequency(40)
				stepper.ChangeDutyCycle(0)
				condicion = False
				#Apagar motor
			else:
				stepper.ChangeFrequency(40)
				stepper.ChangeDutyCycle(50)
		if(condicion):
			masa = hx.get_weight(3)		
		print(masa)
	print(masa)
	print("Bye...")

except(KeyboardInterrupt,SystemExit):
	stepper.stop()
	cleanAndExit()
finally:
	GPIO.cleanup()

