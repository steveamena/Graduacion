
import RPi.GPIO as GPIO
import time
import sys
import math
#import threading

from hx711 import HX711
global contador
contador = 0
	
GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(8,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(7,GPIO.OUT,initial=GPIO.LOW)

def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()

def inRangeCoerce(dato,minimo,maximo):
	if(dato<minimo):
		return minimo
	if(dato>maximo):
		return maximo
	return dato
#call backs
def interrupcion(channel):
	#Funcion para interrupcion del Rasp
#	global temporizador
	global contador
	contador = contador + 1
	print(contador)

def ejecucionTiempo():
	global temporizador
	global contador
	GPIO.output(8,GPIO.HIGH)
	time.sleep(0.0005)
	GPIO.output(8,GPIO.LOW)
	print("hola")
	#temporizador.cancel()
	return

#Interrupciones
valor = False

fase = 140
fase = inRangeCoerce(fase,0.0,150.0)
disparo = fase/21600
GPIO.add_event_detect(24, GPIO.BOTH,callback = interrupcion,bouncetime=1)

try:
	print "hola"
	while True:
		time.sleep(1)
		pass
		
except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
finally:
        GPIO.cleanup()
        
