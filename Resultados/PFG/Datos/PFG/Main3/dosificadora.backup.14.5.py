##Definicion de clase dosificadora
##Steve Mena Navarro
## 6 Marzo 2019
## Ultima revision 10 Abril 2019
## 17 Abril 2019: Se incluyo la implementacion en còdigo C++ para los sensores y los perifericos

import RPi.GPIO as GPIO		#Libreria de manejo GPIO
#from hx711 import HX711	#Libreria de manejo celdas de carga
from Scale import Scale
import time
import numpy as np			#Libreria de arreglos
from matplotlib import pyplot as plt

class Dosificadora:
	def __init__(self):
		#Crear el objeto de la clase dosificadora	

		##Convenciones: axxxx: a significa atributo
					#Con-> Concentrado
					#Min-> Mineral
					#Lev-> Levadura
						
		#Puertos de control para las valvulas
		self.avTolva		= 2
		self.avMineral		= 16
		self.avLevadura		= 27
		
		#Puertos de asignacion de las celdas de carga
		self.alsensorC1		= (11,9) 	#Formato tupla: (dt,sck)
		self.alsensorC2		= (22,10)	
		self.alsensorC3		= (24,23)
		self.alsensorC4		= (12,6)
		self.alsensorML		= (19,13)
		
		#Puertos control de motores
		self.amCon			= (7,8)		#Formato tupla: (Encendido, velocidad)
		self.amMin			= (20,21) 	#Formato tupla: (velocidad, sentido)
		self.amLev			= (25,26)
		
		#Sensibilidades celdas de carga
		self.asMin	 		= 1030.3320
		self.asLev		 	= 2563.3821
		self.asC1			= 1
		self.asC2			= 1
		self.asC3			= 1
		self.asC4			= 1
		self.asConc			= 53.2201
		
		#Valores de Tara para cada celda de carga
		self.asZeroMin		= 0
		self.asZeroLev		= 0
		self.asZeroC1		= 0
		self.asZeroC2		= 0
		self.asZeroC3		= 0
		self.asZeroC4		= 0
		
		#Masas objetivo
		self.aConObj		= 1
		self.aMinObj		= 1
		self.aLevObj		= 1
		self.aMasaObj		= [self.aConObj,self.aMinObj,self.aLevObj]
		
		#Parametros del filtro tamizador y media movil
		self.aPeso_kbuffer 	= [[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0]]	#Formato lista [Con,Min,Lev]
		self.aSk			= [0.0,	0.0,	0.0	] 		#Formato listas [Con,Min,Lev]
		self.aContador		= [0,	0,	0]
		self.aDato_k_1		= [0.0,	0.0,	0.0	]
		self.aX_k_1			= [0.0,	0.0,	0.0	]
		
		#Valores para algoritmo de control
		self.aMultiplo		= [0.8,	0.8,	0.8] 		#Formato listas [Con,Min,Lev]
		self.aDeltaRef		= [0.0,	0.0,	0.0]
		
		self.aInt				= [0.0,	0.0,	0.0]
		self.aKp				= [0.03, 	0.0,	0.0]
		self.aKi				= [0.0,		0.0,	0.0]
		self.aKd				= [0.0,		0.0,	0.0]
		
		self.aVk_1				= 0.0
		self.aEk_1				= 0.0
		self.aYk_1 				= 0.0
		self.aDk_1				= 0.0
		self.aUk_1				= 0
		self.aRk_1				= 0

		self.aSimk_21 			= 0
		self.aSimk_20   		= 0
		self.aSimk_19			= 0
		self.aSimk_18 			= 0
		self.aSimk_17 			= 0
		self.aSimk_16 			= 0
		self.aSimk_15 			= 0
		self.aSimk_14   		= 0
		self.aSimk_13			= 0
		self.aSimk_12 			= 0
		self.aSimk_11 			= 0
		self.aSimk_10 			= 0
		self.aSimk_9  			= 0
		self.aSimk_8  			= 0
		self.aSimk_7  			= 0
		self.aSimk_6  			= 0
		self.aSimk_5  			= 0
		self.aSimk_4  			= 0
		self.aSimk_3  			= 0
		self.aSimk_2   			= 0
		self.aSimk_1			= 0
		
		self.aInt_Retardo		= 0
		self.aTcontador			= 0						
		self.aDoCalcularKp		= [True,	True,	True]
		self.aPWM				= [0.0,	0.0,	0.0]

		self.aTrayectoriaCon	= np.zeros(600)
		self.aAceleracion		= [300.0,0.0,0.0]
		#Otros atributos
		self.asText			= "________________" 	#Separador de Textos
		self.minCon			= 39.0					#Menor ciclo de PWM permitido para el concentrado
		self.maxCon			= 99.0					#Mayor ciclo de PWM permitido para el concentrado
		self.razon			= [60.0,50.0,10.0]			#Mayor tasa de cambio permitida por el filtro tamizador
													#Formato lista [Con,Min,Lev]
		self.aConCrucero	= 70.0					#Velocidad crucero motor Con
		self.aConMin		= 60.0					#Minima velocidad para mover el motor

	def __del__(self):
	#Metodo destructor de objeto
		nombre = self.__class__.__name__
		print(nombre, "Destruido")
		
	def inicializarPuertos(self):
		#Encargado de iniciar el estado de los puertos de RPi.
		
		print("\n________________\nIniciando puertos\n________________\n")
	#Configurar puertos
		#Valvulas
		GPIO.setup(self.avTolva,GPIO.OUT)
		GPIO.setup(self.avMineral,GPIO.OUT)
		GPIO.setup(self.avLevadura,GPIO.OUT)
			
		#Motores
			#Concentrado
		GPIO.setup(self.amCon[0],GPIO.OUT)
		GPIO.setup(self.amCon[1],GPIO.OUT)
			
			#Mineral
		GPIO.setup(self.amMin[0],GPIO.OUT)
		GPIO.setup(self.amLev[0],GPIO.OUT)
		
			#Levadura
		GPIO.setup(self.amMin[1],GPIO.OUT)
		GPIO.setup(self.amLev[1],GPIO.OUT)
		
		#Colocar todos los puertos en BAJO "LOW".
		GPIO.output(self.avTolva,0)
		GPIO.output(self.avMineral,0)
		GPIO.output(self.avLevadura,0)
		
		GPIO.output(self.amCon[0],0)
		GPIO.output(self.amCon[1],0)
		
		GPIO.output(self.amMin[0],0)
		GPIO.output(self.amMin[1],0)
		
		GPIO.output(self.amLev[0],0)
		GPIO.output(self.amLev[1],0)
		
	def inicializarMotores(self):
	#Iniciar el estado de los motores 
		#Frecuencia de PWM
		self.amMinPWM	= GPIO.PWM(self.amMin[0],300) 	#Formato tupla: (velocidad, sentido)
		self.amLevPWM	= GPIO.PWM(self.amLev[0],300)	#Formato tupla: (velocidad, sentido)
		self.amConPWM	= GPIO.PWM(self.amCon[1],250)
		
		##Iniciar PWM en valor 0
		self.amMinPWM.start(0)
		self.amLevPWM.start(0)
		self.amConPWM.start(0)
		
	def inicializarCeldas(self):
	#Inciar celdas de carga
		print("\n________________\nIniciando celdas de carga\n________________\n")
			#Formato tupla: self.alsensorA	=	(dt,sck)
			
			#Celda de carga Concentrado C1
		self.ahxC1 	= Scale(self.alsensorC1[0], self.alsensorC1[1], 1, 80)
			#Celda de carga Concentrado C2
		self.ahxC2 	= Scale(self.alsensorC2[0], self.alsensorC2[1], 1, 80)
			#Celda de carga Concentrado C3
		self.ahxC3 	= Scale(self.alsensorC3[0], self.alsensorC3[1], 1, 80)
			#Celda de carga Concentrado C4
		self.ahxC4 	= Scale(self.alsensorC4[0], self.alsensorC4[1], 1, 80)		
			#Celda de carga Levadura Mineral
		self.ahxML	= Scale(self.alsensorML[0], self.alsensorML[1], 	1, 80)
		
		self.resetearCeldas()
		
	def encenderMotores(self,motor):
		#Metodo que activa los motores
		#Entrada: 	self-> 	Objeto propio de python
		#			motor->	Selector del motor: 
		#					Con: Concentrado, Min: mineral Lev: levadura
		
		if (motor=='Con'):
			if self.aConObj!=0:
				#Encendido motor Con
				velocidad = 99#self.aConCrucero
				self.amConPWM.ChangeDutyCycle(velocidad)
				GPIO.output(self.amCon[0],1)
			else:
				print("Masa es 0, concentrado no encendido")
			return
			
		if (motor=='Min'):
			if self.aMinObj!=0:
				self.amMinPWM.ChangeFrequency(750)
				self.amMinPWM.ChangeDutyCycle(50)
			else:
				print("Masa igual a 0, mineral no encendido")
			return
			
		if (motor=='Lev'):
			if self.aLevObj!=0:
				self.amLevPWM.ChangeFrequency(750)
				self.amLevPWM.ChangeDutyCycle(50)
			else:
				print("Masa igual a 0, levadura no encendido")
			return
			
		else:
			print("Motor no encontrado")
		
	def desacelerarMotores(self,motor):
		#Metodo que desacelera los motores
		if(motor=='Con'):
			velocidad = self.aConMin
			self.amConPWM.ChangeDutyCycle(velocidad)
			return
			
		if(motor=='Min'):
			self.amMinPWM.ChangeFrequency(200)
			self.amMinPWM.ChangeDutyCycle(50)
			return
			
		if(motor=='Lev'):
			self.amLevPWM.ChangeFrequency(200)
			self.amLevPWM.ChangeDutyCycle(50)
			return
			
		else:
			print("Motor no encontrado")
			return
			
	def apagarMotores(self,motor,condicion):
		#Detener motores
		#Entradas: motor: 	Seleccion del motor deseado
		#					Con -> Concentrado
		#					Min -> Mineral
		#					Lev -> Levadura
		#		Condicion:	Indica si el motor no fue apagado en la iteracion anterior
		if (motor=='Con'):
			GPIO.output(self.amCon[0],0)
			self.amConPWM.stop()
			if condicion:
				print("Concentrado apagado")
			return
			
		if (motor=='Min'):
			self.amMinPWM.ChangeFrequency(50)
			self.amMinPWM.ChangeDutyCycle(0)
			if condicion:
				print("Mineral apagado")
			return
			
		if (motor=='Lev'):
			self.amLevPWM.ChangeFrequency(50)
			self.amLevPWM.ChangeDutyCycle(0)
			if condicion:
				print("Levadura apagado")
			return
			
		else:
			print("Motor no encontrado")
			return
	
	def abrirCerrarValvulas(self,valvula,condicion):
		#Metodo de abrir y cerrar valvulas
		#Entradas:	valvula: 
		#				Tolv -> Puerta de la tolva Romana
		#				Min	->	Compuerta del mineral
		#				Lev ->	Compuerta levadura
		#			condicion:
		#				0 	->	Valvula cerrada
		#				1	->	Valvula abierta
		
		if (valvula=='Tolv'):
			GPIO.output(self.avTolva,condicion)
			return
		
		if (valvula =='Min'):
			GPIO.output(self.avMineral,condicion)
			return
		
		if (valvula =='Lev'):
			GPIO.output(self.avLevadura,condicion)
			return
			
		else:
			print("Valvula incorrecta")
	
	def cambiarSensibilidad(self,celda,sensibilidad):
	#Metodo para cambiar la sensibilidad de la celda de carga: (depuracion) 
		#Formato de celda: 'Min','Lev','A','B'
		#Entradas: celda: A1, A2, B1, B2, Min, Lev
		print("Cambiando sensibilidad")
		if (celda=='A1'):
			self.asA1 = sensibilidad
			self.axA.select_channel(channel='A')
			self.axA.set_scale_ratio(sensibilidad)
			return
			
		if (celda=='A2'):
			self.asA2 = sensibilidad	
			self.axA.select_channel(channel='B')
			self.axA.set_scale_ratio(sensibilidad)
			return
			
		if (celda=='B1'):
			self.asB1 = sensibilidad
			self.axB.select_channel(channel='A')
			self.axB.set_scale_ratio(sensibilidad)
			return
			
		if (celda=='B2'):
			self.asB2 = sensibilidad
			self.axB.select_channel(channel='B')
			self.axB.set_scale_ratio(sensibilidad)
			return
			
		if (celda=='Min'):
			self.asMin = sensibilidad
			self.axML.select_channel(channel='A')
			self.axML.set_scale_ratio(sensibilidad)
			return
			
		if (celda=='Lev'):
			self.asLev = sensibilidad
			self.axML.select_channel(channel='A')
			self.axML.set_scale_ratio(sensibilidad)
			return
			
		else:
			print("Celda no encontrada")
			
	def leerMineral(self,lecturas):
	#Leer el peso del mineral en gramos.
		#Entrada: lecturas -> Cantidad de veces que el sensor se lee antes de retornar
		
		#Mineral puerto A del sensor
		masaMin = -((self.ahxML.weighOnce())-self.asZeroMin)/self.asMin
		return masaMin
	
	def leerLevadura(self,lecturas):
	#Leer el peso del mineral en gramos.
		#Entrada: lecturas -> Cantidad de veces que el sensor se lee antes de retornar
		masaLev = (self.ahxML.weighOnce()-self.asZeroLev)/self.asLev
		return masaLev
	
	def leerConcentrado(self,lecturas):
	#Leer el peso del concentrado en gramos.
		#Entrada: lecturas -> Cantidad de veces que el sensor se lee antes de retornar
		
		Conc1 	= self.ahxC1.weighOnce()-self.asZeroC1
		
		Conc2 	= self.ahxC2.weighOnce()-self.asZeroC2
		
		Conc3 	= self.ahxC3.weighOnce()-self.asZeroC3
				
		Conc4	= -(self.ahxC4.weighOnce()-self.asZeroC4)
				
		Conc = (Conc1+Conc2+Conc3+Conc4)/(4*self.asConc)
		#Nota: De momento se estan leyendo solo las celdas de los puertos A del concentrado
		#		las celdas B presetan problemas de retardos en las lecturas
		return float(Conc)
	
	def cerrarSteppers(self):
	#Metodo para apagar puertos de velocidad de los motores 
			self.amMinPWM.stop()
			self.amLevPWM.stop()
			self.amConPWM.stop()
			
	def leer4Concentrado(self):
	#Metodo para leer por separado cada celda de carga del concentrado 	(depuracion)
		Conc1 	= self.ahxC1.weighOnce()-self.asZeroC1
		
		Conc2 	= self.ahxC2.weighOnce()-self.asZeroC2
		
		Conc3 	= self.ahxC3.weighOnce()-self.asZeroC3
				
		Conc4	= -(self.ahxC4.weighOnce()-self.asZeroC4)
		print("%d\t%d\t%d\t%d"%(Conc1,Conc2,Conc3,Conc4))
		
	def leer4ConcentradoRaw(self,lecturas):
	#Metodo para leer cada celda del concentrado sin restar tara 		(depuracion)
		Conc1 	= self.ahxC1.weighOnce()
		
		Conc2 	= self.ahxC2.weighOnce()
		
		Conc3 	= self.ahxC3.weighOnce()
				
		Conc4	= self.ahxC4.weighOnce()
				
		print("%d\t%d\t%d\t%d"%(Conc1,Conc2,Conc3,Conc4))
		
	def tararConcentrado(self,imprimir= False,lecturas=30):
		#Metodo para tarar los amplificadores del concentrado
		if imprimir:
			print("Tarando")
		
		self.asZeroC1 	= self.ahxC1.weigh(80)
		 
		self.asZeroC2 	= self.ahxC2.weigh(80)
		
		self.asZeroC3 	= self.ahxC3.weigh(80)
		
		self.asZeroC4 	= self.ahxC4.weigh(80)
		
		if imprimir:
			print("Tara del concentrado\n%d\t%d\t%d\t%d\t"%
			(self.asZeroC1,self.asZeroC2,self.asZeroC3,self.asZeroC4))

	def tararMineral(self,printVal=False,lecturas=30):
	#Metodo para tarar mineral
	
		self.asZeroMin = self.ahxML.tare(lecturas,False)
		if printVal:
			print("\tTara del mineral %d"%(self.asZeroMin))
	
	def tararLevadura(self,printVal=False,lecturas = 30):
	#Metodo para tarar levdura
		self.asZeroMin = self.ahxML.tare(lecturas,False)
		if printVal:
			print("\tTara de la levadura %d"%(self.asZeroMin))

	def filtradorTamizador(self,dato,alimento):
	#Metodo para filtrar y tamizar los valores de las celdas de carga
	#Se aplica un filtro de media movil con tres periodos,
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
			concentrado 		= self.aSk[0]/5
			self.aPeso_kbuffer[0][self.aContador[0]] = datoT
			
			#Mover el contador y retrasar las muestras
			self.aContador[0] 	+=	1
			self.aDato_k_1[0]	= dato
			self.aX_k_1[0]		= datoT
			
			if self.aContador[0] 	== 5:
				self.aContador[0] 	= 0
			return concentrado
			
		if alimento == 'Min':
			#Tamizar
			if ((abs(dato-self.peso_k_1[1]))>self.razon[1]):
				dato = self.peso_k_1[1]
				print("Tamizado")
			#Filtrar
			mineral			 	= (dato+self.peso_k_1[1]+self.peso_k_2[1])/3
			self.peso_k_2[1]	= self.peso_k_1[1]
			self.peso_k_1[1]	= mineral
			return mineral
		
		if alimento == 'Lev':
			#Tamizar
			if ((abs(dato-self.peso_k_1[2]))>self.razon[2]):
				dato = self.peso_k_1[2]
				print("Tamizado")
			#Filtrar
			levadura 			= (dato+self.peso_k_1[2]+self.peso_k_2[2])/3
			self.peso_k_2[2]	= self.peso_k_1[2]
			self.peso_k_1[2]	= levadura
			return levadura
			
		else:
			print("Alimento no encontrado")
			
	def	inRangeCoerce(self,dato, minimo = 0.0, maximo = 100.0):
	#Metodo que limita los valores de una variable
		if dato > maximo:
			return maximo
			
		if dato < minimo:
			return minimo
		
		else:
			return dato
			
	def normalizarVelocidadConcentrado(self,dato):
	#Metodo para normalizar los valores del concentrado
		#Debido a la electronica, el valor de PWM permitido es entre 39 y 99.
		#Fuera de esos valores comienza a presentarse comportamiento erratico.
		dato = self.inRangeCoerce(dato,0,100)
		dato = (self.maxCon-self.minCon)/100 * dato + self.minCon
		return dato
	
	#Metodos para resumir bloques de la secuencia
	def tararCeldas(self):
	#Metodo para tarar todas las cedas de carga. Permite no hacerlo desde el main
		self.leerMineral(80)
		print("________________\nTarando Concentrado\n________________\n")
		self.tararConcentrado(80,True)
		print("Zero A1 ",self.asZeroC1)
		print("Zero A2 ",self.asZeroC2)
		print("Zero B1 ",self.asZeroC3)
		print("Zero B2 ",self.asZeroC4)
		
		print("________________\nTarando Mineral\n________________\n")
		self.tararMineral(80)
		print("________________\nTarando Levadura\n________________\n")
		self.tararLevadura(80)

	def resetearCeldas(self):
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
		
		print("Reseteando celdas de carga Mineral y Levadura")
		self.ahxML.turnOff()
		time.sleep(0.5)
		self.ahxML.turnOn()
		time.sleep(0.5)
		
	def filtroButterWorth(self,xk):
		self.yk = (0.7769*self.xk_1 #- 0.007079*self.xk_2
			 + 0.2231*self.yk_1) #- 0.000002 * self.yk_2)
		#Retrasar muestras
		#self.xk_4	= self.xk_3
		#self.xk_3	= self.xk_2
		self.xk_2	= self.xk_1	  
		self.xk_1	= xk	
		
		#self.yk_4	= self.yk_3
		#self.yk_3	= self.yk_2
		self.yk_2	= self.yk_1	  
		self.yk_1	= self.yk
		return self.yk	
		
	def controlPI(self,yk):
		#Comienza algoritmo de control
		
		#Estimacion de la velocidad
		#vk = yk-self.aYk_1+0.6703*self.aVk_1
		
		#Estimacion del retardo
		uk_1 = self.inRangeCoerce(self.aUk_1-0.5,0,1)
		rk = 104.5*(uk_1)+0.8389*self.aRk_1
		#rk = self.inRangeCoerce(rk,0,10000)
		self.aInt_Retardo = ((rk+self.aRk_1)/2)*0.05+self.aInt_Retardo
		#self.aInt_Retardo = self.inRangeCoerce(self.aInt_Retardo,0,10000)
		
		#Estimacion del error
		ek = (self.aTrayectoriaCon[self.aTcontador]-yk)*1-self.aInt_Retardo+self.aSimk_20;
		#Estimacion del control PID
		pk = self.aKp[0]*(ek)
		ik = self.aInt[0]+ek*0.05*self.aKi[0]
		dk = ((self.aKd[0]*100)*(ek-self.aEk_1)+self.aDk_1)/(1+100*0.05)
		pidk = pk+ik+dk
		pidk = 100*self.inRangeCoerce(pidk,0,0.99)
		self.amConPWM.ChangeDutyCycle(pidk) 
		#Termina algoritmo de control
		#Calcula referencia para el futuro
		
		#Retrasar las muestras simuladas
		self.aSimk_20 = self.aSimk_19
		self.aSimk_19 = self.aSimk_18
		self.aSimk_18 = self.aSimk_17
		self.aSimk_17 = self.aSimk_16
		self.aSimk_16 = self.aSimk_15
		self.aSimk_15 = self.aSimk_14
		self.aSimk_14 = self.aSimk_13
		self.aSimk_13 = self.aSimk_12
		self.aSimk_12 = self.aSimk_11
		self.aSimk_11 = self.aSimk_10
		self.aSimk_10 = self.aSimk_9
		self.aSimk_9 = self.aSimk_8
		self.aSimk_8 = self.aSimk_7
		self.aSimk_7 = self.aSimk_6
		self.aSimk_6 = self.aSimk_5
		self.aSimk_5 = self.aSimk_4
		self.aSimk_4 = self.aSimk_3
		self.aSimk_3 = self.aSimk_2
		self.aSimk_2 = self.aSimk_1
		self.aSimk_1 = self.aInt_Retardo
		
		#Retrasa las muestras
		#self.aVk_1 = vk
		self.aYk_1 = yk
		self.aDk_1 = dk
		self.aEk_1 = ek
		self.aInt[0] = ik
		self.aPWM[0] = pidk		
		self.aUk_1 = pidk
		self.aRk_1 = rk 	
		#Anti Windup
		if (self.aKi[0]==0):
			limite = 30000
		else:
			limite = 100/self.aKi[0]
		
		self.aInt[0]	= self.inRangeCoerce(self.aInt[0],-limite,limite)
		if (self.aTcontador == 599):
			print("Terminado")
		else:
			self.aTcontador += 1

	def generadorTrayectoria(self):
		print("Generando Trayectorias")
		a	= self.aAceleracion[0]
		t2 	= self.aMasaObj[0]/a-2
		tf 	= t2+4
		k 	= 0
		m1 	= 0.5*a
		m2 	= a*t2+m1
		tiempo = np.arange(0.05,30.05,0.05)
		k 	= 0
		mk 	= np.zeros(600)
		
		#Inicia la generacion de la trayectoria
		t = 0
		while t < 30:
			t = tiempo[k]
			if t <=1:
				mk[k] 	= (a/2)*t*t
			if ((1<t) and (t<=(t2+1))):
				mk[k]	= a*(t-1)+m1
			if ((t2+1<t) and (t<=tf)):
				mk[k]	= -a/6*(t-t2-1)*(t-t2-1)+a*(t-t2-1)+m2
			elif (t>tf):
				mk[k]	= self.aMasaObj[0]
			k += 1
		print("Trayectoria generada")
		self.aTrayectoriaCon = mk
				
				
 	
		
