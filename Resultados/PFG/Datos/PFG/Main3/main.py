##Programa prueba de concepto
##Steve Mena Navarro
##8/03/2019
##PFG
##Ultima revsion 10/04/2019
##Incluida la libreria pulsethread y las implementaciones en C++
##GanaCenter
##16/05/2019: Movida la libreria dosificadora a /Testing/
##Limpiado el codigo de cosas que no sirven o que estan obsoletas

import RPi.GPIO as GPIO							#Manejo GPIO en RPi 
import time, sys

from Testing.dosificadora import Dosificadora	#importar clase Dosificadora
from Scale import Scale							#Clase que maneja las celdas de
												#carga desde C++
from cowlist import Cowlist						#Maneja archivos Excel con el balance de vacas

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
espacio= "________________"

#Multiplo del peso meta para desacelerar motores
multiplo = 0.80

#Programa principal
print("___Programa prototipo de UberCow____\n")
excel = True 
#Si Excel es false, el programa no pide la lista de vacas

try:

	#iniciar GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	#Inciar la secuencia
	if excel:
		print(espacio)
		print("Cargando archivo de balances")
		print(espacio)
	
		listaVacas 		= Cowlist(59,3)
		nombreArchivo 	= listaVacas.get_name_from_Interface()
		listaVacas.loadData(nombreArchivo)
		
	#Crear objeto Dosificadora
	UberCow 	= Dosificadora()
	UberCow.inicializarPuertos()
	UberCow.inicializarMotores()
	UberCow.inicializarCeldas()
	
	print("________________\nSecuencia Iniciada\n________________\n")

	while True:
		UberCow.peso_k_1 	= [0,0,0]
		UberCow.peso_k_2 	= [0,0,0]
		if excel:
			vaca 		= input("Digite el numero de vaca a preparar ")
			racion		= listaVacas.get_cow_ration(vaca)
			print("Numero de vaca\tVapFeed\t\tMultiplex Oro")
			print("________________")
			print("%d\t\t%f\t%f\n"%(racion[0],racion[1],racion[2]))
			input("Presione una tecla para continuar ")
		
		else:

		#Lectura de los datos del usuario.
			conObj		= 4000.0#float(input("Digite la cantidad de concentrado en g "))
			minObj 		= 100.0#float(input("Digite la cantidad de mineral en g "))
			levObj		= 100.0#float(input("Digite la cantidad de levadura en g "))
		UberCow.tararCeldas()
		UberCow.aMasaObj[0]		= conObj
		UberCow.aConObj			= conObj
		
		print("________________\nEncendiendo motores\n________________\n")
		UberCow.encenderMotores("Con")
		#UberCow.encenderMotores("Min")
		#UberCow.encenderMotores("Lev")
		
		ontador = 0
		print("%sMasas%s"%(espacio,espacio))
		print("Concentrado\t\tMineral\t\tLevadura\n%s%s"%(espacio,espacio))		
		while(condicion):
			masaConc 		= UberCow.leerConcentrado(4)
			masaConcF		= UberCow.filtradorTamizador(masaConc,'Con')
						
			masaMin			= 0#UberCow.leerMineral(1)
			masaMin			= UberCow.filtradorTamizador(masaMin,'Min')

			masaLev			= 0#UberCow.leerLevadura(1)		
			masaLev			= UberCow.filtradorTamizador(masaLev,'Lev')			

			#print("%s\t%s\t%s"%(str(masaConc),str(masaMin),str(masaLev)))
			UberCow.controlPDCon(masaConcF)
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
			"""	
			#Stepper Levadura
			#UberCow.controlPDLev(masaLev)
			#print(str(masaLev), "\t",str(UberCow.aPWM[2]))
			if (masaLev>=levObj):
				UberCow.apagarMotores('Lev',condicionLev)
				condicionLev 	= False
			
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
	
	

