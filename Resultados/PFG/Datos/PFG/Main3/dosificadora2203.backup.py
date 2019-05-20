##Definicion de clase dosificadora
##Steve Mena Navarro
## 6 Marzo 2019

import RPi.GPIO as GPIO		#libreria de manejo GPIO
from hx711 import HX711		#Libreria de manejo celdas de carga

class Dosificadora:
	def __init__(self):
		##Inicializar objeto dosificadora
		##Convenciones: axxxx: a: atributo, m metodo. 
		
		#Valvulas
		self.avTolva	 	= 2
		self.avMineral 		= 16
		self.avLevadura 	= 27
		
		#Celdas de carga
		self.alsensorA		= (11,9) 	#Formato tupla: (dt,sck)
		self.alsensorB		= (22,10)
		self.alsensorML		= (19,13)
		#Motores
		self.amCon			= 7
		self.amMin			= (20,21) 	#Formato tupla: (velocidad, sentido)
		self.amLev			= (25,26)
		
		#Sensibilidades celdas de carga
		self.asMin	 		= 1048.5	
		self.asLev		 	= 2881.96
		self.asA1			= 1
		self.asA2			= 1
		self.asB1			= 1
		self.asB2			= 1
		self.asConc			= 55.254
				
		self.asZeroMin		= 1
		self.asZeroLev		= 1
		self.asZeroA1		= 1
		self.asZeroA2		= 1
		self.asZeroB1		= 1
		self.asZeroB2		= 1
		
		#Atributos masas targets
		self.asConcObj		= 1
		self.asConcObj		= 1
		self.asConcObj		= 1
		
		#Atributos filtro
		self.aAnterior		= [0,0,0] 		#Formato de lista [conc,min,lev]
		self.aRazon 		= [100,100,100]	#Formato lista [conc,min,lev]
		#Otros atributos
		self.asText			= "________________"
		#Otros atributos
		
	def inicializarPuertos(self):
		print("\n________________\nIniciando puertos\n________________\n")
		#Valvulas
		GPIO.setup(self.avTolva,GPIO.OUT)
		GPIO.setup(self.avMineral,GPIO.OUT)
		GPIO.setup(self.avLevadura,GPIO.OUT)
			
		#Motores
		GPIO.setup(self.amCon,GPIO.OUT)
		
		GPIO.setup(self.amMin[0],GPIO.OUT)
		GPIO.setup(self.amLev[0],GPIO.OUT)
		
		GPIO.setup(self.amMin[1],GPIO.OUT)
		GPIO.setup(self.amLev[1],GPIO.OUT)
		
		#Colocar todos los puertos en BAJO
		GPIO.output(self.avTolva,0)
		GPIO.output(self.avMineral,0)
		GPIO.output(self.avLevadura,0)
		
		GPIO.output(self.amCon,0)
		
		GPIO.output(self.amMin[0],0)
		GPIO.output(self.amMin[1],0)
			
		GPIO.output(self.amLev[0],0)
		GPIO.output(self.amLev[1],0)
		
	def inicializarSteppers(self):
		self.amMinPWM	= GPIO.PWM(self.amMin[0],300) 	#Formato tupla: (velocidad, sentido)
		self.amLevPWM	= GPIO.PWM(self.amLev[0],300)	#Formato tupla: (velocidad, sentido)
		##Apagar PWM
		self.amMinPWM.start(0)
		self.amLevPWM.start(0)
		
	def inicializarCeldas(self):
		print("\n________________\nIniciando celdas de carga\n________________\n")		
			#Formato tupla: self.alsensorA	=	(dt,sck)
			#Sensibilidaddes: self.asMin, asB#
		self.ahxA 	= HX711(dout=self.alsensorA[0], pd_sck=self.alsensorA[1], 
							gain=64, select_channel='A')
		self.ahxB 	= HX711(dout=self.alsensorB[0], pd_sck=self.alsensorB[1],
							gain=64, select_channel='A')
		self.ahxML	= HX711(dout=self.alsensorML[0], pd_sck=self.alsensorML[1], 
							gain=64, select_channel='A')
							
			#Inicializa, resetea y tara A
		print("\n________________\nConfigurando Amplificador A\n________________\n")		
		print("\tReseteando...")
		self.ahxA.reset() 			#Resetear celdas de carga
					# Asegurar que reseteo fue exitoso

		
		self.ahxA.set_gain(gain		= 64)  	#Configurar ganancia para el canal A
		self.ahxA.select_channel(channel='A')
		self.ahxA.set_reference_unit(1)		#Calibrar celda A
		self.asZeroA1 = self.ahxA.tare(1)	#Tarar celda de carga

		self.ahxA.select_channel(channel='B')
		self.asZeroA2 = self.ahxA.tare(1)
		self.ahxA.set_offset(0)
		
		self.ahxA.select_channel(channel='A')
		print('\tConfigurado\n')		
		##Configurar amplificador B
		#Inicializa, resetea y tara B
		print("\n________________\nConfigurando Amplificador B\n________________\n")
		print("\tReseteando...")
		self.ahxA.reset() 						#Resetear celdas de carga
												# Asegurar que reseteo fue exitoso
		self.ahxB.set_gain(gain		= 64)  		#Configurar ganancia para el canal A
		self.ahxB.select_channel(channel='A')
		self.ahxB.set_reference_unit(1)			#Calibrar celda A
		self.asZeroB1 = self.ahxA.tare(1)		#Tarar celda de carga
		
		self.ahxB.select_channel(channel='B')
		self.asZeroB2 = self.ahxA.tare(1)
		self.ahxB.set_offset(0)
		
		self.ahxB.select_channel(channel='A')
		print('\tConfigurado\n')		
		
		##Configurar amplificador Min Lev
		#Inicializa, resetea y tara Min Lev
		print("\n________________\n\Configurando Amplificador Min Lev\n________________\n")
		print("\tReseteando...")
		self.ahxML.reset() 						#Resetear celdas de carga
												# Asegurar que reseteo fue exitoso
		print('\tConfigurado')
		
		self.ahxML.set_gain(gain		= 64)  	#Configurar ganancia para el canal A
		self.ahxML.select_channel(channel='A')
		self.ahxML.set_reference_unit(1)		#Calibrar celda A
		self.asZeroMin = self.ahxML.tare(1)		#Tarar celda de carga
		
		self.ahxML.select_channel(channel='B')
		self.asZeroLev = self.ahxML.tare(1)
		self.ahxML.set_offset(0)
		
		self.ahxML.select_channel(channel='A')
	
	def encenderMotores(self,motor):
		#De momento que unicamente se apague y encienda el motor
		if (motor=='Con'):
			GPIO.output(self.amCon,1)
			#print("Motor Concentrado encendido")
			return
		if (motor=='Min'):
			self.amMinPWM.ChangeFrequency(750)
			self.amMinPWM.ChangeDutyCycle(50)
			#print("Motor Mineral encendido")
			return
		if (motor=='Lev'):
			self.amLevPWM.ChangeFrequency(750*2)
			self.amLevPWM.ChangeDutyCycle(50)
			#print("Motor Levadura encendido")
		else:
			print("Motor no encontrado")
	
	def desacelararSteppers(self,motor):
		if(motor=='Min'):
			self.amMinPWM.ChangeFrequency(200)
			self.amMinPWM.ChangeDutyCycle(50)
			return
		if(motor=='Lev'):
			self.amLevPWM.ChangeFrequency(200*2)
			self.amLevPWM.ChangeDutyCycle(50)
		else:
			print "Stepper no encontrado"
			
	def apagarMotores(self,motor,condicion):
		#De momento que unicamente se apague y encienda el motor
		if (motor=='Con'):
			GPIO.output(self.amCon,0)
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
	
	def abrirCerrarValvulas(self,valvula,condicion):
		#Metodo abrir y cerrar valvulas, valvula es caracter, condicion es numerico
		
		if (valvula=='Tolv'):
			GPIO.output(self.avTolva,condicion)
			return
		if (valvula =='Min'):
			GPIO.output(self.avMineral,condicion)
			return
		if (valvula =='Lev'):
			GPIO.output(self.avLevadura,condicion)
		else:
			print("Valvula incorrecta")
	
	def cambiarSensibilidad(self,celda,sensibilidad):
		#Formato de celda: 'Min','Lev','A','B'
		print("Cambiando sensibilidad")
		if (celda=='A1'):
			self.asA1 = sensibilidad
			self.axA.select_channel(channel='A')
			self.axA.set_scale_ratio(sensibilidad)
		if (celda=='A2'):
			self.asA2 = sensibilidad	
			self.axA.select_channel(channel='B')
			self.axA.set_scale_ratio(sensibilidad)
		if (celda=='B1'):
			self.asB1 = sensibilidad
			self.axB.select_channel(channel='A')
			self.axB.set_scale_ratio(sensibilidad)
		if (celda=='B2'):
			self.asB2 = sensibilidad
			self.axB.select_channel(channel='B')
			self.axB.set_scale_ratio(sensibilidad)
		if (celda=='Min'):
			self.asMin = sensibilidad
			self.axML.select_channel(channel='A')
			self.axML.set_scale_ratio(sensibilidad)
		if (celda=='Lev'):
			self.asLev = sensibilidad
			self.axML.select_channel(channel='A')
			self.axML.set_scale_ratio(sensibilidad)
		else:
			print("Celda no encontrada")

	def leerMineral(self,lecturas):
		#Mineral puerto A del sensor
		self.ahxML.select_channel(channel='A')
		masaMin = -((self.ahxML.get_value(lecturas))-self.asZeroMin)/self.asMin
		
		return masaMin
	
	def leerLevadura(self,lecturas):
		self.ahxML.select_channel(channel='B')
		masaLev = (self.ahxML.get_value(3)-self.asZeroLev)/self.asLev
		return masaLev
	
	def leerConcentrado(self,lecturas):
		self.ahxA.select_channel(channel='A')
		Conc1 	= (self.ahxA.get_value(lecturas)-self.asZeroA1)
		
		#self.ahxA.select_channel(channel='B')
		#Conc2	= (self.ahxA.get_value(lecturas)-self.asZeroA2)
		
		self.ahxB.select_channel(channel='A')
		Conc3 	= (self.ahxB.get_value(lecturas)-self.asZeroB1)
				
		#self.ahxB.select_channel(channel='B')
		#Conc4	= (self.ahxB.get_value(1)-self.asZeroB1)
				
		Conc = (Conc1+Conc3)/self.asConc
		
		return Conc
	
	def cerrarSteppers(self):
			self.amMinPWM.stop()
			self,amLevPWM.stop()
		
	def leer4Concentrado(self):
		self.ahxA.select_channel(channel='A')
		Conc1 	= (self.ahxA.get_value(1)-self.asZeroA1)
		
		self.ahxA.select_channel(channel='B')
		Conc2	= (self.ahxA.get_value(1)-self.asZeroA2)
		
		self.ahxB.select_channel(channel='A')
		Conc3 	= (self.ahxB.get_value(1)-self.asZeroB1)
				
		#self.ahxB.select_channel(channel='B')
		Conc4	= (self.ahxB.get_value(1)-self.asZeroB1)

		print("%d\t%d\t%d\t%d"%(Conc1,Conc2,Conc3,Conc4))
	
	
	def leer4ConcentradoRaw(self):
		self.ahxA.select_channel(channel='A')
		Conc1 	= (self.ahxA.get_value(1))
		
		self.ahxA.select_channel(channel='B')
		Conc2	= (self.ahxA.get_value(1))
		
		self.ahxB.select_channel(channel='A')
		Conc3 	= (self.ahxB.get_value(1))
				
		self.ahxB.select_channel(channel='B')
		Conc4	= (self.ahxB.get_value(1))

		print("%d\t%d\t%d\t%d"%(Conc1,Conc2,Conc3,Conc4))
		return
		
	def tararConcentrado(self):
		#Funcion que tara los amplificadores por aparte
		self.ahxA.select_channel(channel='A')
		self.asZeroA1 = self.ahxA.get_value(10)
		
#		self.ahxA.select_channel(channel='B')
#		self.asZeroA2 = self.ahxA.get_value(10)
		
		self.ahxB.select_channel(channel='A')
		self.asZeroB1 = self.ahxB.get_value(10)

		self.ahxB.select_channel(channel='B')
		self.asZeroB2 = self.ahxB.get_value(10)
		
	def tararMineral(self):
		self.ahxML.select_channel(channel='A')
		self.asZeroMin = self.ahxML.get_value(10)

		print("\tTara del mineral %d"%(self.asZeroMin))
	def tararLevadura(self):
		self.ahxML.select_channel(channel='B')
		self.asZeroMin = self.ahxML.get_value(10)

	def tamizarLectura(self,lectura,celda):
		if (celda=='Min'):
			anterior 	= self.aAnterior
			razon 		= self.aRazon
			if ((lectura-anterior[1])<razon[1]):
				self.asAnterior = lectura
				return lectura
			else:
				return self.asAnterior
			
		
	
		print("\tTara de la levadura %d"%(self.asZeroMin))
