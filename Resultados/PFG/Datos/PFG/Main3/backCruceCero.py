
import RPi.GPIO as GPIO
import time
import sys
import math
from hx711 import HX711

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

GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.IN)
GPIO.setup(8,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(7,GPIO.OUT,initial=GPIO.LOW)

contador = 0
fase = 140
fase = inRangeCoerce(fase,0.0,150.0)
disparo = fase/21600
try:

	while True:
		valor = GPIO.input(12)
		if (valor):
			contador = contador + 1
			time.sleep(disparo)
			GPIO.output(8,GPIO.HIGH)
			time.sleep(0.0005)
			GPIO.output(8,GPIO.LOW)
		if (contador == 120):
			GPIO.output(7,GPIO.HIGH)
			fase = fase - 10.0
			fase = inRangeCoerce(fase,20.0,150.0)
			disparo = fase/21600
			print(fase)
			print("a")
			contador = 0
			print("o")
		if (fase==20.0):
			time.sleep(5)
			break
	while True:
		valor = GPIO.input(12)
		if (valor):
			contador = contador + 1
			time.sleep(disparo)
			GPIO.output(8,GPIO.HIGH)
			time.sleep(0.0005)
			GPIO.output(8,GPIO.LOW)
		if (contador == 120):
			GPIO.output(7,GPIO.HIGH)
			fase = fase + 5.0
			fase = inRangeCoerce(fase,20.0,150.0)
			disparo = fase/21600
			print(fase)
			print("a")
			contador = 0
			print("o")
		if (fase==150):
			GPIO.output(8,GPIO.LOW)
			GPIO.output(7,GPIO.LOW)
       # hx.power_down()
       # hx.power_up()
       # time.sleep(0.1)
except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
finally:
        GPIO.cleanup()
        
