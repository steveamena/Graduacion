##Programa para dosificar el mineral con compuerta accionada neumaticamente
##STeve Mena Navarro PFG

#Start importing the required libraries
import RPi.GPIO as GPIO
import time
import sys
##Importar las librerias para la celda de carga
from hx711 import HX711

##Inicializar valvula
pValvula = 3
#funcion para inicializar la celda de carga.
def startLoadCell(sensibilidad):
	hx = HX711(19,13)
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

##Funcion para encender y apagar valvula
def abrirValvula(valv):
	for i in range(2):
		GPIO.output(valv,1)
		time.sleep(1)
		GPIO.output(valv,0)
		time.sleep(1)

##Inicia el codigo main
#Inicializar el GPIO
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(21,GPIO.OUT)
	GPIO.setup(20,GPIO.OUT)
	GPIO.setup(pValvula,GPIO.OUT)

	#Configura "el sentido de giro"
	GPIO.output(21,GPIO.LOW)
	#GPIO.output(21,GPIO.LOW)
	stepper = GPIO.PWM(20,300)
	stepper.start(0)
	GPIO.output(pValvula,0)
	masaObjetivo = 60.5 	#Variable que almacena la masa objetivo
	print("Motor arrancado...")
	#Obtener la primera medicion de la masa
	hx = startLoadCell(-2120.829)
	masa = hx.get_weight()
	print("Celda de carga arrancada...")
##While que arranca el motor mientras haga falta masa	
	condicion = True
	v_1=0
	v_2=0
	while True:
#		stepperSpeed(stepper,60)
		if(masa/masaObjetivo<0.85):
			stepper.ChangeFrequency(750)
			stepper.ChangeDutyCycle(50)
		else:
			if(masa/masaObjetivo>=1):
				stepper.ChangeFrequency(50)
				stepper.ChangeDutyCycle(0)
				condicion = False
				#Apagar motor
				abrirValvula(pValvula)
				break
			else:
				stepper.ChangeFrequency(150)
				stepper.ChangeDutyCycle(50)
		if(condicion):
			v = hx.get_weight(6)
			masa=(v+v_1+v_2)/3
			v_2 = v_1
			v_1= v
		print(masa)
	print("Bye...")

except(KeyboardInterrupt,SystemExit):
	stepper.stop()
	cleanAndExit()
finally:
	GPIO.cleanup()

