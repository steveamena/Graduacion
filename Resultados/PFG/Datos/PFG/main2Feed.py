##Codigo para dosificar mineral y levadura completos
##Steve Mena Navarro PFG 
# -----------------------
#Importar librerias requeridas

import RPi.GPIO as GPIO
import time
import sys
##Importar las librerias para la celda de carga
from hx711 import HX711

#funcion para inicializar la celda de carga.
def startLoadCell(sensibilidad,mineral):
	if(mineral):
		hx = HX711(4,17)
	else:
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
	GPIO.output(27,GPIO.LOW)
	#GPIO.output(21,GPIO.LOW)
	stepperMin = GPIO.PWM(20,300)
	stepperLev = GPIO.PWM(22,300)
	
	stepperMin.start(0)
	stepperLev.start(0)

	objMineral = 90.0	#Variable que almacena la masa objetivo
	objLevadura = 4.0
	sMineral = -2097.8
	sLevadura = 11734.0

	print("Motor arrancado...")
	#Crear los objetos de celdas de cargas
	hxMin = startLoadCell(sMineral,True)
	hxLev = startLoadCell(sLevadura,False)
	masaMin = hxMin.get_weight()
	masaLev =hxLev.get_weight()
	print("Celdas de carga arrancadas...")
##While que arranca el motor mientras haga falta masa	
	condicionMin = True
	condicionLev = True

	while True:
	#-----Condiciones del motor de mineral
#		stepperSpeed(stepper,60)
		if(masaMin/objMineral<0.90):
			stepperMin.ChangeFrequency(750)
			stepperMin.ChangeDutyCycle(50)

		else:
			if(masaMin/objMineral>=1):
				stepperMin.ChangeFrequency(50)
				stepperMin.ChangeDutyCycle(0)
				condicionMin = False
				#Apagar motor
			else:
				stepperMin.ChangeFrequency(200)
				stepperMin.ChangeDutyCycle(50)
		#---Condiciones motor de levadura ----
		if(masaLev/objLevadura<0.9):
			stepperLev.ChangeFrequency(750)
			stepperLev.ChangeDutyCycle(50)
		else:
			if(masaLev/objLevadura>=1):
				stepperLev.ChangeFrequency(50)
				stepperLev.ChangeDutyCycle(0)
				condicionLev = False
			else:
				stepperLev.ChangeFrequency(200)
				stepperLev.ChangeDutyCycle(50)
		if(condicionMin):
			masaMin = hxMin.get_weight(3)
		if(condicionLev):
			masaLev = hxLev.get_weight(3)
		print(masaLev)
		print(masaMin)
		
	print("Bye...")

except(KeyboardInterrupt,SystemExit):
	stepperLev.stop()
	stepperMin.stop()
	cleanAndExit()
finally:
	GPIO.cleanup()

