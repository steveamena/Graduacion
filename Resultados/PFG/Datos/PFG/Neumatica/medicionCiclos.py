#This is the file which opens and clse the gates
#Steve Mena Navarro
#ITCR
#22 Febrero 2019
#Programa que abre y cierra la compuerta de la tolva romana para medir
#cuantos ciclos de trabajo soporta 150 psi de tanque a presion de
#trabajo de 80 psi.

import RPi.GPIO as GPIO
import time

#Abrir archivo de conteo y actualizarlo cada ciclo de trabajo.
#Cada 10 ciclos de trabajo archivo se cierra y se abre para salvar cambios.
#Se cierra y se abre cada  segundo, medio segundo abrir y medio segundo cerrar
archivo = open("Conteo_ciclos.txt","w+")
archivo.write("Presion inicial: 150 psi, presion de trabajo 80 psi\nCiclos de apertura y cierre cada segundo")
archivo.write("Tiempo\tCiclos\n")
puerto = 2
start = time.time()
####
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(puerto,GPIO.OUT)
	conteo = 0
	while True:
		for i in range(10):
			GPIO.output(puerto,1)
			time.sleep(0.5)
			GPIO.output(puerto,0)
			time.sleep(0.5)
			print(conteo)
			print('\n')
			transcurso = time.time()-start
			archivo.write("%s\t%s\n" %(transcurso,conteo))
			conteo = conteo+1
		archivo.close()
		archivo = open('Conteo_ciclos.txt',"a+")
		#time.sleep(2)
finally:
	GPIO.cleanup()
	print("Bye")


