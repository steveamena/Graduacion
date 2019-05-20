##Programa prueba de concepto
##Steve Mena Navarro
##8/03/2019
##PFG
##Ultima revsion 10/04/2019
##Incluida la libreria pulsethread y las implementaciones en C++
##GanaCenter

import RPi.GPIO as GPIO					#Importar clase GPIO 
import time, sys
#import numpy					#Importar clases time, sys & Numpy
#from hx711 import HX711  				#Importar la clase HX711
from dosificadora import Dosificadora	#importar clase Dosificadora
from Scale import Scale
from cowlist import Cowlist

#Definicion de funciones
def cleanAndExit(UberCow):
	#Limpia los puerto GPIO al finalizar
	print("\tLimpiando...")
	GPIO.cleanup()
	print("\tBye...")
	del UberCow
	sys.exit()
		
#Condicion de parada para cada secuencia de la dosificacion
condicion 		= True
condicionConc 	= True
condicionMin 	= True
condicionLev 	= True
#Multiplo del peso meta para desacelerar motores
multiplo = 0.80

#Iniciar GPIO del RPi
print("___Programa prototipo de UberCow____\n")
try:
	#iniciar GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	#Inciar la secuencia
	print("________________\nCargando archivo de balances\n________________\n")
	#listaVacas 		= Cowlist(59,3)
	#nombreArchivo 	= listaVacas.get_name_from_Interface()
	#listaVacas.loadData(nombreArchivo)
	
	#Crear objeto Dosificadora
	UberCow 	= Dosificadora()
	UberCow.inicializarPuertos()
	UberCow.inicializarMotores()
	UberCow.inicializarCeldas()
	
	print("________________\nSecuencia Iniciada\n________________\n")

	while True:
		UberCow.peso_k_1 	= [0,0,0]
		UberCow.peso_k_2 	= [0,0,0]
		
		#vaca 		= input("Digite el numero de vaca a preparar ")
		#racion		= listaVacas.get_cow_ration(vaca)
		print("\n")
		print("Numero de vaca\tVapFeed\t\tMultiplex Oro")
		print("________________")
		print("%d\t\t%f\t%f\n"%(racion[0],racion[1],racion[2]))
		
		input("Presione una tecla para continuar ")
		
		#Lectura de los datos del usuario.
		conObj		= 4000.0#float(input("Digite la cantidad de concentrado en g "))
		minObj 		= 100.0#float(input("Digite la cantidad de mineral en g "))
		levObj		= 100.0#float(input("Digite la cantidad de levadura en g "))
		UberCow.tararCeldas()
		input("")

		
		print("\n____________ Masas ____________\n")
		print("Concentrado\t\tMineral\t\tLevadura\n________________________________")
		##Inicia secuencia del usuario
		UberCow.aMasaObj[0]		= conObj
		UberCow.aConObj			= conObj
		
		print("________________\nEncendiendo motores\n________________\n")
		UberCow.encenderMotores("Con")
		UberCow.encenderMotores("Min")
		UberCow.encenderMotores("Lev")
		contador = 0

		while(condicion):
			
			masaConc = 0.0
			for i in range(4):
				masaConc += UberCow.leerConcentrado(1)
			masaConc 		= masaConc/4
			masaConcF		= UberCow.filtradorTamizador(masaConc,'Con')
						
			masaMin			= #UberCow.leerMineral(1)
			masaMin			= UberCow.filtradorTamizador(masaMin,'Min')

			masaLev			= UberCow.leerLevadura(1)/2		
			masaLev			= UberCow.filtradorTamizador(masaLev,'Lev')			

			#print("%s\t%s\t%s"%(str(masaConc),str(masaMin),str(masaLev)))
			UberCow.controlPD(masaConcF)
			print(str(masaConcF), "\t",str(UberCow.aPWM[0]))
			
			if (masaConcF>=conObj):
				UberCow.apagarMotores('Con',condicionConc)
				condicionConc 	= False	
			"""	
			#Stepper Mineral
			if((masaMin<minObj) and condicionMin):
				if(masaMin>multiplo*minObj):
					UberCow.desacelerarMotores('Min')
			else:
				UberCow.apagarMotores('Min',condicionMin)
				condicionMin 	= False
				
			#Stepper Levadura
			if((masaLev<levObj) and condicionLev):
				if(masaLev>multiplo*levObj):
					UberCow.desacelerarMotores('Lev')
			else:
				UberCow.apagarMotores('Lev',condicionLev)
				condicionLev 	= False
			"""
			
			#Activar pistones
			if(not(condicionConc)and(not(condicionMin))and(not(condicionLev))):
				for i in range(2):
					time.sleep(1)
					UberCow.abrirCerrarValvulas('Min',1)
					UberCow.abrirCerrarValvulas('Lev',1)
					time.sleep(1)
					UberCow.abrirCerrarValvulas('Min',0)
					UberCow.abrirCerrarValvulas('Lev',0)
			
				time.sleep(1)
				UberCow.abrirCerrarValvulas('Tolv',1)
				time.sleep(4)
				UberCow.abrirCerrarValvulas('Tolv',0)
				time.sleep(1)
				UberCow.abrirCerrarValvulas('Tolv',1)
				time.sleep(1)
				UberCow.abrirCerrarValvulas('Tolv',0)
				print("\tDosifcado")
				break
		
		seguir = input("Desea dosificar otra racion? (1/0) ")
		if (seguir==0):
			break
		elif (seguir==1):
			condicion 		= True
			condicionConc 	= True
			condicionMin 	= True
			condicionLev 	= True
		else:
			print("Caracter no reconocido Abortando")
			break

except(KeyboardInterrupt,SystemError,SystemExit):
	cleanAndExit(UberCow)

finally:
	GPIO.cleanup()
	print("Bye")
	
	

