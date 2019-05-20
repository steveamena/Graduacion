##Programa prueba de concepto
##Steve Mena Navarro
##8/03/2019
##PFG
##Ultima revsion 10/04/2019
##GanaCenter

import RPi.GPIO as GPIO					#Importar clase GPIO 
import time, sys, numpy					#Importar clases time, sys & Numpy
from hx711 import HX711  				#Importar la clase HX711
from dosificadora import Dosificadora	#importar clase Dosificadora
#import openpyxl

#Definicion de funciones
def cleanAndExit(UberCow):
	#Limpia los puerto GPIO al finalizar
	print("\tLimpiando...")
	GPIO.cleanup()
	print("\tBye...")
	del UberCow
	sys.exit()

def crearListaCeros(filas=58,columnas=3):
	#Crea lista de ceros
	arreglo = [0] * filas
	for i in range(filas):
		arreglo[i] = [None] * columnas
	return arreglo


def obtenerListaVacas(nombreExcel):
	#Obtiene lista de vacas (liberia openpyxl)
	#Funcion para obtener el numero de vaca en el libro de excel
	listaVacas = crearListaCeros()
	print("Cargado libro de balances")
	libro = openpyxl.load_woorbook(nombreExcel)		#Obtener libro excel
	hojaL1 = excel_document.get_sheet_by_name('L1')	#Obtener hoja excel
	
	i = 0
	multiple_cells = sheet['C6':'C64']				#Obtener numeros de vaca
	for row in multiple_cells:
		for cell in row:
			listaVacas[0,i] = cell.value
			i = i+1

	i = 0
	multiple_cells = sheet['H6':'H64']				#Obtener cantidad de VFeed
	for row in multiple_cells:
		for cell in row:
			listaVacas[1,i] = cell.value	
			i = i+1
	i = 0
	multiple_cells = sheet['K6':'K64']				#Obtener cantidad de multiplex
	for row in multiple_cells:
		for cell in row:
			listaVacas[2,i] = cell.value	
			i = i+1
	return listaVacas

	
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

	#Crear objeto Dosificadora
	UberCow 	= Dosificadora()
	UberCow.inicializarPuertos()
	UberCow.inicializarMotores()
	UberCow.inicializarCeldas()
	
	print("________________\nSecuencia Iniciada\n________________\n")

	while True:
		UberCow.peso_k_1 	= [0,0,0]
		UberCow.peso_k_2 	= [0,0,0]
		UberCow.ahxA.set_offset(0)
		UberCow.ahxB.set_offset(0)
		time.sleep(2)
	
		#Lectura de los datos del usuario.
		conObj		= input("Digite la cantidad de concentrado en g ")
		minObj 		= input("Digite la cantidad de mineral en g ")
		levObj		= input("Digite la cantidad de levadura en g ")
		UberCow.tararCeldas()
		
		print("________________\nEncendiendo motores\n________________\n")
		UberCow.encenderMotores("Con")
		UberCow.encenderMotores("Min")
		UberCow.encenderMotores("Lev")
		
		print("\n____________ Masas ____________\n")
		print("Concentrado\t\tMineral\t\tLevadura\n________________________________")
		##Inicia secuencia del usuario
		while(condicion):
		
			masaConc 		= UberCow.leerConcentrado(6)
			masaConc		= UberCow.filtradorTamizador(masaConc,'Con')
		
			masaMin			= UberCow.leerMineral(6)
			masaMin			= UberCow.filtradorTamizador(masaMin,'Min')

			masaLev			= UberCow.leerLevadura(6)		
			masaLev			= UberCow.filtradorTamizador(masaLev,'Lev')			

			print("%s\t%s\t%s"%(str(masaConc),str(masaMin),str(masaLev)))
			
			if((masaConc<conObj) and (condicionConc)):
				if ((masaConc>0.6*conObj)):
					UberCow.desacelerarMotores('Con')
			else:
				UberCow.apagarMotores('Con',condicionConc)
				condicionConc 	= False
				
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
	
	

