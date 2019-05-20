##Definicion de clase para depurar las diferentes partes de la maquina
##Steve Mena Navarro PFG
## 16 Mayo 2019
## GC@2019
##Control de cambios
## 16/05/2019: Se agregaron los metodos para probar la tolva romana
## Se decidio agregar los metodos que no estan agregados aqui a dosificadora
## para no usar mas esta clase mas.

import RPi.GPIO as GPIO		#Libreria de manejo GPIO
#from hx711 import HX711	#Libreria de manejo celdas de carga
from Scale import Scale
import time
import numpy as np			#Libreria de arreglos

class Testing:
	def __init__(self):
		#Atributos de las celdas de carga del concentrado
		self.alsensorC1		= (11,9) 	#Formato tupla: (dt,sck)
		self.alsensorC2		= (22,10)	
		self.alsensorC3		= (24,23)
		self.alsensorC4		= (12,6)
		self.alsensorML		= (19,13)
		
		self.asZeroC1		= 0
		self.asZeroC1		= 0
		self.asZeroC1		= 0
		self.asZeroC1	 	= 0
		self.asZeroMin		= 0
		self.asZeroLev		= 0
		
		self.asConc			= 53.2201
		self.asMin	 		= 1030.3320
		self.asLev		 	= 2563.3821
		
		#Atributos del filtro
		self.aDato_k_1		= [0.0,		0.0,	0.0]
		self.razon			= [60.0,50.0,10.0]	
		self.aX_k_1			= [0.0,		0.0,	0.0]
		
		self.aSk			= [0.0,		0.0,	0.0]
		self.aPeso_kbuffer	= np.zeros((3,20),dtype=np.float32)
		self.aContador		= [0,		0,		0]
		
		#Otros atributos
		self.aEspacio		= "_________________"

	def __del__(self):
		nombre = self.__class__.__name__
		print(nombre, "Destruido")

	def InicializarCeldasTR(self):
		#Inicializa las celdas de carga del concentrado
		self.ahxC1 	= Scale(self.alsensorC1[0], self.alsensorC1[1], 1, 80)
		#Celda de carga Concentrado C2
		self.ahxC2 	= Scale(self.alsensorC2[0], self.alsensorC2[1], 1, 80)
		#Celda de carga Concentrado C3
		self.ahxC3 	= Scale(self.alsensorC3[0], self.alsensorC3[1], 1, 80)
		#Celda de carga Concentrado C4
		self.	ahxC4 	= Scale(self.alsensorC4[0], self.alsensorC4[1], 1, 80)
	
	def InicializarCeldasML(self):
		#Inicializa las celdas de carga del mineral Levadura
		self.ahxML	= Scale(self.alsensorML[0], self.alsensorML[1], 	1, 80)
		
	def ResetearCeldasTR(self):
		print("Reseteando celdas de carga concentrado")
		#Celdas del concentrado
		self.ahxC1.turnOff()
		time.sleep(0.5)
		self.ahxC1.turnOn()
		time.sleep(0.5)
		
		self.ahxC1.turnOff()
		time.sleep(0.5)
		self.ahxC1.turnOn()
		time.sleep(0.5)
		
		self.ahxC2.turnOff()
		time.sleep(0.5)
		self.ahxC2.turnOn()
		time.sleep(0.5)
		
		self.ahxC3.turnOff()
		time.sleep(0.5)
		self.ahxC3.turnOn()
		time.sleep(0.5)
		
		self.ahxC4.turnOff()
		time.sleep(0.5)
		self.ahxC4.turnOn()
		time.sleep(0.5)		
	
	def ResetearCeldasML(self):
		print("Reseteando celdas de carga concentrado")
		#Celdas del concentrado
		self.ahxML.turnOff()
		time.sleep(0.5)
		self.ahxML.turnOn()
			
	def LeerConcentrado(self,lecturas):
	#Leer el peso del concentrado en gramos.
		#Entrada: lecturas -> Cantidad de veces que el sensor se lee antes de retornar
		concentrado = 0
		for i in range(lecturas):
			Conc1 	= self.ahxC1.weighOnce()-self.asZeroC1
			
			Conc2 	= self.ahxC2.weighOnce()-self.asZeroC2
			
			Conc3 	= self.ahxC3.weighOnce()-self.asZeroC3
					
			Conc4	= -(self.ahxC4.weighOnce()-self.asZeroC4)
					
			Conc = (Conc1+Conc2+Conc3+Conc4)/(4*self.asConc)
			concentrado += Conc
		concentrado = concentrado/lecturas
		return float(concentrado)
	
	def LeerMineral(self,lecturas):

		#Leer el peso del mineral en gramos.
		#Entrada: lecturas -> Cantidad de veces que el sensor se lee antes de retornar
		#Mineral puerto A del sensor
		masaMin = -((self.ahxML.weighOnce())-self.asZeroMin)/self.asMin
		return masaMin
		
	def FiltroMediaTamizador(self,dato,alimento,periodos=5):
	#Metodo para filtrar y tamizar los valores de las celdas de carga
	#Se aplica un filtro de media movil con n periodos,
	#luego se eliminan las lecturas que presenten cambios abruptos respecto de los valores predecesores.
		if alimento == 'Con':
			
			#Tamizar
			if ((abs(dato-self.aDato_k_1[0]))>self.razon[0]):
				datoT = self.aX_k_1[0]
				#print("Tamizado")
			else:
				datoT = dato
			
			#Filtrar
			self.aSk[0] 		= self.aSk[0]-self.aPeso_kbuffer[0][self.aContador[0]]+datoT
			concentrado		 		= self.aSk[0]/periodos
			self.aPeso_kbuffer[0][self.aContador[0]] = datoT
			#Calcular filtro de media movil en linea
			self.aContador[0] 	+=	1
			self.aDato_k_1[0]	= dato
			self.aX_k_1[0]		= datoT
			
			if self.aContador[0] 	== periodos:
				self.aContador[0] 	= 0
			return concentrado
			
		if alimento == 'Min':
			#Tamizar
			if ((abs(dato-self.peso_k_1[1]))>self.razon[1]):
				datoT = self.peso_k_1[1]
				print("Tamizado")
			else:
				datoT = dato
			
			#Filtrar
			self.aSk[1] 		= self.aSk[1]-self.aPeso_kbuffer[1][self.aContador[1]]+datoT
			mineral		 		= self.aSk[1]/periodos
			self.aPeso_kbuffer[1][self.aContador[1]] = datoT
			
			#Mover el contador y retrasar las muestras
			self.aContador[1] 	+=	1
			self.aDato_k_1[1]	= dato
			self.aX_k_1[1]		= datoT
			
			if self.aContador[1] 	== periodos:
				self.aContador[1] 	= 0
			return mineral
			
		if alimento == 'Lev':
			#Tamizar
			if ((abs(dato-self.aDato_k_1[2]))>self.razon[2]):
				datoT = self.aX_k_1[2]
				#print("Tamizado")
			else:
				datoT = dato
			
			#Filtrar
			self.aSk[2] 		= self.aSk[2]-self.aPeso_kbuffer[2][self.aContador[2]]+datoT
			levadura	 		= self.aSk[2]/periodos
			self.aPeso_kbuffer[2][self.aContador[2]] = datoT
			
			#Mover el contador y retrasar las muestras
			self.aContador[2] 	+=	1
			self.aDato_k_1[2]	= dato
			self.aX_k_1[2]		= datoT
			
			if self.aContador[2] 	== periodos:
				self.aContador[2] 	= 0
			return levadura
			
		else:
			print("Alimento no encontrado")
			
	def TararConcentrado(self,imprimir= False,lecturas=30):
		#Metodo para tarar los amplificadores del concentrado
		if imprimir:
			print("Tarando")
		
		self.asZeroC1 	= self.ahxC1.weigh(lecturas)
		 
		self.asZeroC2 	= self.ahxC2.weigh(lecturas)
		
		self.asZeroC3 	= self.ahxC3.weigh(lecturas)
		
		self.asZeroC4 	= self.ahxC4.weigh(lecturas)
		
		if imprimir:
			print("Tara del concentrado\n%d\t%d\t%d\t%d\t"%
			(self.asZeroC1,self.asZeroC2,self.asZeroC3,self.asZeroC4))

	def ProbarCeldasTR(self, tiempo):
		#Obtiene muestras de la celda de carga por una cantidad determinada de tiempo
		print(self.aEspacio)
		print("Probando celdas de carga Tolva Romana")
		print(self.aEspacio)
		
		self.InicializarCeldasTR()
		self.ResetearCeldasTR()
		self.TararConcentrado(False,80)
		
		print("Sin filtro\tCon Filtro")
		tic = time.time()
		while True:
			Con 	= self.LeerConcentrado(4)
			
			#Calcular filtro de media movil en linea
			ConF 	= self.FiltroMediaTamizador(Con,'Con',5)
			print("%f\t%f"%(Con,ConF))
			toc 	= time.time()
			
			#Condicion de parada para el ciclo
			if ((toc-tic)>=tiempo):
				break
	
	def ProbarCeldasMinLev(self,tiempo):
		#Obtiene muestras de la celda de carga por una cantidad determinada de tiempo
		print(self.aEspacio)
		print("Probando celdas de carga Mineral-Levadura")
		print(self.aEspacio)
		
		self.InicializarCeldasML()
		self.ResetearCeldasML()
		self.TararMinLev(False,80)
		
		print("Sin filtro\tCon Filtro")
		tic = time.time()
		while True:
			Min 	= self.LeerMineral(80)
			
			#Calcular filtro de media movil en linea
			ConF 	= self.FiltroMediaTamizador(Con,'Con',5)
			print("%f\t%f"%(Con,ConF))
			toc 	= time.time()
			
			#Condicion de parada para el ciclo
			if ((toc-tic)>=tiempo):
				break
