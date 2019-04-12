##Definicion de clase dosificadora
##Steve Mena Navarro
## 6 Marzo 2019
## Ultima revision 10 Abril 2019

import RPi.GPIO as GPIO		#libreria de manejo GPIO
from hx711 import HX711		#Libreria de manejo celdas de carga

class Dosificadora:
	def __init__(self):
		#Crear el objeto de la clase dosificadora	

		##Convenciones: axxxx: a significa atributo
		 			#Con-> Concentrado
					#Min-> Mineral
					#Lev-> Levadura
						
		#Puertos de control para las valvulas
		self.avTolva	 	= 2
		self.avMineral 		= 16
		self.avLevadura 	= 27
		
		#Puertos de asignación de las celdas de carga
		self.alsensorA		= (11,9) 	#Formato tupla: (dt,sck)
		self.alsensorB		= (22,10)	
		self.alsensorML		= (19,13)
		
		#Puertos control de motores
		self.amCon			= (7,8)		#Formato tupla: (Encendido, velocidad)
		self.amMin			= (20,21) 	#Formato tupla: (velocidad, sentido)
		self.amLev			= (25,26)
		
		#Sensibilidades celdas de carga
		self.asMin	 		= 1030.3320
		self.asLev		 	= 2563.3821
		self.asA1			= 1
		self.asA2			= 1
		self.asB1			= 1
		self.asB2			= 1
		self.asConc			= 50.380
		
		#Valores de Tara para cada celda de carga
		self.asZeroMin		= 0
		self.asZeroLev		= 0
		self.asZeroA1		= 0
		self.asZeroA2		= 0
		self.asZeroB1		= 0
		self.asZeroB2		= 0
		
		#Masas objetivo
		self.aConObj		= 1
		self.aMinObj		= 1
		self.aLevObj		= 1
		
		#Parámetros del filtro de media móvil
		self.peso_k_1		= [0,0,0] 	#Formato de lista [Con,Min,Lev]
		self.peso_k_2 		= [0,0,0]	#Formato lista [Con,Min,Lev]
		
		#Otros atributos
		self.asText			= "________________" 	#Separador de Textos
		self.minCon			= 39					#Menor ciclo de PWM permitido para el concentrado
		self.maxCon			= 99					#Mayor ciclo de PWM permitido para el concentrado
		self.razon			= [800,50,10]			#Mayor tasa de cambio permitida por el filtro tamizador
													#Formato lista [Con,Min,Lev]
		self.aConCrucero	= 70					#Velocidad crucero motor Con
		self.aConMin		= 60					#Minima velocidad para mover el motor

	def __del__(self):
	#Metodo destructor de objeto
		nombre = self.__class__.__name__
		print nombre, "Destruido"
		
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
			#Sensibilidaddes: self.asMin, asB#
			#Celda de carga Concentrado A
		self.ahxA 	= HX711(dout=self.alsensorA[0], pd_sck=self.alsensorA[1], 
							gain=64, select_channel='A')
			#Celda de carga Concentrado B
		self.ahxB 	= HX711(dout=self.alsensorB[0], pd_sck=self.alsensorB[1],
							gain=64, select_channel='A')
			#Celda de carga Mineral y levadura.
		self.ahxML	= HX711(dout=self.alsensorML[0], pd_sck=self.alsensorML[1], 
							gain=64, select_channel='A')
		
		#Inicializa, resetea y tara A
		
		print("\n________________\nConfigurando Amplificador C1\n________________\n")
		print("\tReseteando...")
		#Resetear amplificador C1
		self.ahxA.reset()			 			
		self.ahxA.set_gain(gain	= 64)		  	#Configurar ganancia para el canal A
		self.ahxA.select_channel(channel='A')
		self.ahxA.set_reference_unit(1)			#Resetear calibracion amplificador C1
		self.asZeroA1 = self.ahxA.tare(1)		#Tarar celda de carga C1A

		self.ahxA.select_channel(channel='B')
		self.asZeroA2 = self.ahxA.tare(1)		#Tarar celda de carga C1B
		self.ahxA.set_offset(0)
	
		self.ahxA.select_channel(channel='A')
		print('\tConfigurado\n')		
		
		# -------------------------------------------------------------#
		##Configurar amplificador C2
		#Inicializa, resetea y tara amplificador C2
		print("\n________________\nConfigurando Amplificador C2\n________________\n")
		print("\tReseteando...")
		self.ahxA.reset() 						#Resetear amplificador C2
		self.ahxB.set_gain(gain	= 64)	  		#Configurar ganancia para el canal A
		self.ahxB.select_channel(channel='A')	
		self.ahxB.set_reference_unit(1)			#Resetear calibración amplificador C2
		self.asZeroB1 = self.ahxA.tare(1)		#Tarar celda de carga
		
		self.ahxB.select_channel(channel='B')	
		self.asZeroB2 = self.ahxA.tare(1)
		self.ahxB.set_offset(0)
		
		self.ahxB.select_channel(channel='A')
		print('\tConfigurado\n')		
		
		##Configurar amplificador Min Lev
		#Inicializa, resetea y tara Min Lev
		print("\n________________\nConfigurando Amplificador Min Lev\n________________\n")
		print("\tReseteando...")
		self.ahxML.reset() 						#Resetear amplificador
		print('\tConfigurado')
		
		self.ahxML.set_gain(gain = 64)		  	#Configurar ganancia para el canal A
		self.ahxML.select_channel(channel='A')
		self.ahxML.set_reference_unit(1)		#Calibrar celda A
		self.asZeroMin = self.ahxML.tare(1)		#Tarar celda de carga
		
		self.ahxML.select_channel(channel='B')
		self.asZeroLev = self.ahxML.tare(1)
		self.ahxML.set_offset(0)
		
		self.ahxML.select_channel(channel='A')
	
	def encenderMotores(self,motor):
		#Metodo que activa los motores
		#Entrada: 	self-> 	Objeto propio de python
		#			motor->	Selector del motor: 
		#					Con: Concentrado, Min: mineral Lev: levadura
		
		if (motor=='Con'):
			if self.aConObj!=0:
				#Encendido motor Con
				velocidad = self.aConCrucero
				self.amConPWM.ChangeDutyCycle(velocidad)
				GPIO.output(self.amCon[0],1)
			else:
				print "Masa es 0, concentrado no encendido"
			return
			
		if (motor=='Min'):
			if self.aMinObj!=0:
				self.amMinPWM.ChangeFrequency(750)
				self.amMinPWM.ChangeDutyCycle(50)
			else:
				print "Masa igual a 0, mineral no encendido"
			return
			
		if (motor=='Lev'):
			if self.aLevObj!=0:
				self.amLevPWM.ChangeFrequency(750)
				self.amLevPWM.ChangeDutyCycle(50)
			else:
				print "Masa igual a 0, levadura no encendido"
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
			print "Motor no encontrado"
			return
			
	def apagarMotores(self,motor,condicion):
		#Detener motores
		#Entradas: motor: 	Seleccion del motor deseado
		#					Con -> Concentrado
		#					Min -> Mineral
		#					Lev -> Levadura
		#		Condición:	Indica si el motor no fue apagado en la iteracion anterior
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
		#			condición:
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
		self.ahxML.select_channel(channel='A')
		masaMin = -((self.ahxML.get_value(lecturas))-self.asZeroMin)/self.asMin
		return masaMin
	
	def leerLevadura(self,lecturas):
	#Leer el peso del mineral en gramos.
		#Entrada: lecturas -> Cantidad de veces que el sensor se lee antes de retornar
		self.ahxML.select_channel(channel='B')
		masaLev = (self.ahxML.get_value(lecturas)-self.asZeroLev)/self.asLev
		return masaLev
	
	def leerConcentrado(self,lecturas):
	#Leer el peso del concentrado en gramos.
		#Entrada: lecturas -> Cantidad de veces que el sensor se lee antes de retornar
		self.ahxA.select_channel(channel='A')
		Conc1 	= (self.ahxA.get_value(lecturas)-self.asZeroA1)
		
		#self.ahxA.select_channel(channel='B')
		#Conc2	= (self.ahxA.get_value(lecturas)-self.asZeroA2)
		
		self.ahxB.select_channel(channel='A')
		Conc3 	= (self.ahxB.get_value(lecturas)-self.asZeroB1)
				
		#self.ahxB.select_channel(channel='B')
		#Conc4	= (self.ahxB.get_value(1)-self.asZeroB1)
				
		Conc = (Conc1+Conc3)/self.asConc
		#Nota: De momento se están leyendo solo las celdas de los puertos A del concentrado
		#		las celdas B presetan problemas de retardos en las lecturas
		return Conc
	
	def cerrarSteppers(self):
	#Metodo para apagar puertos de velocidad de los motores 
			self.amMinPWM.stop()
			self.amLevPWM.stop()
			self.amConPWM.stop()
			
	def leer4Concentrado(self):
	#Metodo para leer por separado cada celda de carga del concentrado 	(depuracion)
		self.ahxA.select_channel(channel='A')
		Conc1 	= (self.ahxA.get_value(1)-self.asZeroA1)
		
		self.ahxA.select_channel(channel='B')
		Conc2	= (self.ahxA.get_value(1)-self.asZeroA2)
		
		self.ahxB.select_channel(channel='A')
		Conc3 	= (self.ahxB.get_value(1)-self.asZeroB1)
				
		self.ahxB.select_channel(channel='B')
		Conc4	= (self.ahxB.get_value(1)-self.asZeroB1)

		print("%d\t%d\t%d\t%d"%(Conc1,Conc2,Conc3,Conc4))
		
	def leer4ConcentradoRaw(self,lecturas):
	#Metodo para leer cada celda del concentrado sin restar tara 		(depuracion)
		self.ahxA.select_channel(channel='A')
		Conc1 	= (self.ahxA.get_value(lecturas))
		
		self.ahxA.select_channel(channel='B')
		Conc2	= (self.ahxA.get_value(lecturas))
		
		self.ahxB.select_channel(channel='A')
		Conc3 	= (self.ahxB.get_value(lecturas))
				
		self.ahxB.select_channel(channel='B')
		Conc4	= (self.ahxB.get_value(lecturas))

		print("%d\t%d\t%d\t%d"%(Conc1,Conc2,Conc3,Conc4))
		return
		
	def tararConcentrado(self,lecturas):
		#Metodo para tarar los amplificadores del concentrado
		self.ahxA.select_channel(channel='A')
		self.asZeroA1 = self.ahxA.get_value(lecturas)
		
		self.ahxA.select_channel(channel='B')
		self.asZeroA2 = self.ahxA.get_value(lecturas)
		
		self.ahxB.select_channel(channel='A')
		self.asZeroB1 = self.ahxB.get_value(lecturas)

		self.ahxB.select_channel(channel='B')
		self.asZeroB2 = self.ahxB.get_value(lecturas)
		
	def tararMineral(self):
	#Metodo para tarar mineral
		self.ahxML.select_channel(channel='A')
		self.asZeroMin = self.ahxML.get_value(lecturas)
		print("\tTara del mineral %d"%(self.asZeroMin))
	
	def tararLevadura(self):
	#Metodo para tarar levdura
		self.ahxML.select_channel(channel='B')
		self.asZeroMin = self.ahxML.get_value(30)
		print("\tTara de la levadura %d"%(self.asZeroMin))

	def filtradorTamizador(self,dato,alimento):
	#Metodo para filtrar y tamizar los valores de las celdas de carga
	#Se aplica un filtro de media movil con tres periodos,
	#luego se eliminan las lecturas que presenten cambios abruptos respecto de los valores predecesores.
	
		if alimento == 'Con':
			#Tamizar
			if ((abs(dato-self.peso_k_1[0]))>self.razon[0]):
				dato = self.peso_k_1[0]
				print "Tamizado"
			#Filtrar
			concentrado 		= (dato+self.peso_k_1[0]+self.peso_k_2[0])/3
			self.peso_k_2[0]	= self.peso_k_1[0]
			self.peso_k_1[0]	= concentrado
			return concentrado
			
		if alimento == 'Min':
			#Tamizar
			if ((abs(dato-self.peso_k_1[1]))>self.razon[1]):
				dato = self.peso_k_1[1]
				print "Tamizado"
			#Filtrar
			mineral			 	= (dato+self.peso_k_1[1]+self.peso_k_2[1])/3
			self.peso_k_2[1]	= self.peso_k_1[1]
			self.peso_k_1[1]	= mineral
			return mineral
		
		if alimento == 'Lev':
			#Tamizar
			if ((abs(dato-self.peso_k_1[2]))>self.razon[2]):
				dato = self.peso_k_1[2]
				print "Tamizado"
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
		#Fuera de esos valores comienza a presentarse comportamiento errático.
		dato = self.inRangeCoerce(dato,0,100)
		dato = (self.maxCon-self.minCon)/100 * dato + self.minCon
		return dato
	
	#Metodos para resumir bloques de la secuencia
	def tararCeldas(self):
	#Metodo para tarar todas las cedas de carga. Permite no hacerlo desde el main
		print("________________\nTarando Concentrado\n________________\n")
		self.tararConcentrado()
		print("Zero A1 ",self.asZeroA1)
		print("Zero A2 ",self.asZeroA2)
		print("Zero B1 ",self.asZeroB1)
		print("Zero B2 ",self.asZeroB2)
		
		print("________________\nTarando Mineral\n________________\n")
		self.tararMineral()
		print("________________\nTarando Levadura\n________________\n")
		self.tararLevadura()
	
