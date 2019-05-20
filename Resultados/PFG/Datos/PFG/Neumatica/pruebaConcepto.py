
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

def writeFile(file,array):
	for item in array:
		file.write("%s\n" % item)

#GPIO.setwarnings(False)
hx = HX711(5,6)

GPIO.setmode(GPIO.BCM)
hx.set_reading_format("LSB", "MSB")

hx.set_reference_unit(1)


#Iniciar GPIO puerto
GPIO.setup(26,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
hx.reset()
hx.tare()
val_ant = 0
offset = 0
offset_ant = 0
GPIO.output(26,0)
GPIO.output(13,0)
print("Iniciado")
fileName=input("Digite el nombre del archivo\n")

#Crear el archivo
file = open(fileName,"w")
Data = [None,None]

try:
	startTime = time.time()
	GPIO.output(26,0)
  	while True:
               	val = hx.get_value(1)
		print(val)
		elapTime = time.time()-startTime
		Data.append([elapTime,val])
		if((elapTime>5)and(elapTime<=10)):
			#Momento de poner peso
			GPIO.output(26,1)
		if((elapTime>10)and(elapTime<=15)):
			#Abrir valvula
			GPIO.output(26,0)
			GPIO.output(13,1)
		if((elapTime>15)and(elapTime<=20)):
			#Cerrar valvula
			GPIO.output(26,0)
			GPIO.output(13,0)
		if((elapTime>20)and(elapTime<=25)):
			#Quitar peso
			GPIO.output(26,1)
		if(elapTime>25):
			#Termina
			writeFile(file,Data)
			break
      			hx.power_down()
			file.close()
       # hx.power_up()
       # time.sleep(0.1)
	cleanAndExit()
except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
finally:
        GPIO.cleanup()
        
