##Programa 
##STeve Mena Navarro PFG

#Start importing the required libraries
import RPi.GPIO as GPIO
import time
import sys
##Importar las librerias para la celda de carga
from hx711 import HX711

#funcion para inicializar la celda de carga.
def startLoadCell(sensibilidad):
	hx = HX711(5,6)
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
	##Motor 1
	GPIO.setup(21,GPIO.OUT)
	GPIO.setup(20,GPIO.OUT)
	##Motor 2
	GPIO.setup(22,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)
	#Configura "el sentido de giro"
	GPIO.output(21,GPIO.LOW)
	GPIO.output(22,GPIO.LOW)
	#GPIO.output(21,GPIO.LOW)
	stepper = GPIO.PWM(20,300)
	stepper2 = GPIO.PWM(27,300)
	
	stepper.start(0)
	stepper2.start(0)

	masaObjetivo = 120 	#Variable que almacena la masa objetivo
	print("Motor arrancado...")
	#Obtener la primera medicion de la masa
	hx = startLoadCell(-2097.8)
	masa = hx.get_weight()
	print("Celda de carga arrancada...")
##While que arranca el motor mientras haga falta masa	
	condicion = True
	while True:
#		stepperSpeed(stepper,60)
		if(masa/masaObjetivo<0.90):
			stepper.ChangeFrequency(750)
			stepper.ChangeDutyCycle(50)
			
			stepper2.ChangeFrequency(750)
			stepper2.ChangeDutyCycle(50)
		else:
			if(masa/masaObjetivo>=1):
				stepper.ChangeFrequency(50)
				stepper.ChangeDutyCycle(0)
				
				stepper2.ChangeFrequency(50)
				stepper2.ChangeDutyCycle(0)
				condicion = False
				#Apagar motor
			else:
				stepper.ChangeFrequency(200)
				stepper.ChangeDutyCycle(50)
				
				stepper2.ChangeFrequency(200)
				stepper2.ChangeDutyCycle(50)

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

