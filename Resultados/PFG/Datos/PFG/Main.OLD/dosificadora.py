##Definicion de clase dosificadora
##Nota: Esta clase unicamente funciona en python 2.7.x. 
##		Fue diseñada cuando el concentrado tenia solo dos amplificadores HX711
##		Y tenia que leerse el puerto A y puerto B uno a la vez,
#		de ahi proviene la notacion A1, B1, etc. No funciona si hay un integrado por celda de carga.

import RPi.GPIO as GPIO
from hx711 import HX711

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
		self.asMin	 		= 1
		self.asLev		 	= 1
		self.asA1			= 1
		self.asA2			= 1
		self.asB1			= 1
		self.asB2			= 1
		self.asConc			= 105.902
				
		self.asZeroMin		= 1
		self.asZeroLev		= 1
		self.asZeroA1		= 1
		self.asZeroA2		= 1
		self.asZeroB1		= 1
		self.asZeroB2		= 1
		
		#Otros atributos
		#self.amMinPWM: motoresSteppers
	def inicializarPuertos(self):
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
		print("Iniciando celdas de carga")
			#Formato tupla: self.alsensorA	=	(dt,sck)
			#Sensibilidaddes: self.asMin, asB#
		self.ahxA 	= HX711(dout_pin=self.alsensorA[0], pd_sck_pin=self.alsensorA[1], 
							gain_channel_A=128, select_channel='A')
		self.ahxB 	= HX711(dout_pin=self.alsensorB[0], pd_sck_pin=self.alsensorB[1],
							gain_channel_A=128, select_channel='A')
		self.ahxML	= HX711(dout_pin=self.alsensorML[0], pd_sck_pin=self.alsensorML[1], 
							gain_channel_A=128, select_channel='A')
							
			#Inicializa, resetea y tara A
		print("Configurando A\nReseteando...")
		err = self.ahxA.reset() 			#Resetear celdas de carga
		if err:  					# Asegurar que reseteo fue exitoso
			print('A no lista')
		else:
			print('A lista')

		self.ahxA.set_gain_A(gain		= 64)  	#Configurar ganancia para el canal A
		self.ahxA.select_channel(channel='A')
		self.ahxA.set_scale_ratio(self.asA1)		#Calibrar celda A
		self.ahxA.zero(readings			= 30)
		self.asZeroA1 = self.ahxA._offset_A_64
		
		self.ahxA.select_channel(channel='B')
		self.ahxA.set_scale_ratio(self.asA2)
		self.ahxA.zero(readings			= 30)
		self.asZeroA2 = self.ahxA._offset_B
		
		self.ahxA.select_channel(channel='A')
		print("Amplificador A configurado")
		
		##Configurar amplificador B
		print("Configurando B\nReseteando...")
		err = self.ahxB.reset() 			#Resetear celdas de carga
		if err:  					# Asegurar que reseteo fue exitoso
			print('B no lista')
		else:
			print('B lista')
		self.ahxB.set_gain_A(gain		= 64)  	#Configurar ganancia para el canal A
		self.ahxB.select_channel(channel='A')
		self.ahxB.set_scale_ratio(self.asB1)		#Calibrar celda B
		self.ahxB.zero(readings				= 30)
		self.asZeroB1 = self.ahxB._offset_A_64
		
		self.ahxB.select_channel(channel='B')
		self.ahxB.set_scale_ratio(self.asB2)
		self.ahxB.zero(readings=30)
		self.asZeroB2 = self.ahxA._offset_B
		
		self.ahxB.select_channel(channel='A')
		print("Amplificador B configurado")
		
		#Configurando Mineral y Levadura
			#Inicializa, resetea y tara A
		print("Configurando Min Lev\nReseteando...")
		err = self.ahxML.reset() 			#Resetear celdas de carga
		if err:  					# Asegurar que reseteo fue exitoso
			print('Min Lev no lista')
		else:
			print('Min Lev lista')

		self.ahxML.set_gain_A(gain		= 64)  	#Configurar ganancia para el canal A
		self.ahxML.select_channel(channel='A')
		self.ahxML.set_scale_ratio(self.asMin)		#Calibrar celda A
		self.asZeroMin = self.ahxML.zero(readings			= 30)
		
		self.ahxML.select_channel(channel='B')
		self.ahxML.set_scale_ratio(self.asLev)
		self.asZeroLev = self.ahxML.zero(readings			= 30)
		
		self.ahxML.select_channel(channel='A')
		print("Amplificador Min Lev configurado")
	
	def encenderMotores(self,motor):
		#De momento que unicamente se apague y encienda el motor
		if (motor=='Con'):
			GPIO.output(self.amCon,1)
			print("Motor Concentrado encendido")
			return
		if (motor=='Min'):
			self.amMinPWM.ChangeFrequency(750)
			self.amMinPWM.ChangeDutyCycle(50)
			print("Motor Mineral encendido")
			return
		if (motor=='Lev'):
			self.amLevPWM.ChangeFrequency(750)
			self.amLevPWM.ChangeDutyCycle(50)
			print("Motor Levadura encendido")
		else:
			print("Motor no encontrado")
			
	def apagarMotores(self,motor):
		#De momento que unicamente se apague y encienda el motor
		if (motor=='Con'):
			GPIO.output(self.amCon,0)
			print("Concentrado apagado")
			return
		if (motor=='Min'):
			self.amMinPWM.ChangeFrequency(50)
			self.amMinPWM.ChangeDutyCycle(0)
			print("Mineral apagado")
			return
			
		if (motor=='Lev'):
			self.amLevPWM.ChangeFrequency(50)
			self.amLevPWM.ChangeDutyCycle(0)
			print("Levadura apagado")
			return
		else:
			print("Motor no encontrado")
	
	def abrirCerrarValvulas(self,valvula,condicion):
		#Metodo abrir y cerrar valvulas, valvula es caracter, condicion es numerico
		#Validar si es numerico dato 
		#if (type(valvula !='str')):
		#	print("Tipo de dato incorrecto")
		#else:
		#	print("Tipo de daco correcto")
		
		if (valvula=='Tolv'):
			GPIO.output(self.avTolva,condicion)
			return
		if (valvula =='Min'):
			GPIO.output(self.avMin,condicion)
			return
		if (valvula =='Lev'):
			GPIO.output(self.avLev,condicion)
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
		masaMin = abs(self.ahxML._read()-self.asZeroMin)/self.asMin
		
		return masaMin
	
	def leerLevadura(self,lecturas):
		self.ahxML.select_channel(channel='B')
		masaLev = self.ahxML._read()
		return masaLev
	
	def leerConcentrado(self,lecturas):
		self.ahxA.select_channel(channel='A')
		Conc1 	= abs(self.ahxA._read())
		
		self.ahxA.select_channel(channel='B')
		Conc2	= abs(self.ahxA._read())
		
		self.ahxB.select_channel(channel='A')
		Conc3 	= abs(self.ahxB._read())
				
		self.ahxB.select_channel(channel='B')
		Conc4	= abs(self.ahxB._read())
				
		Conc = ((Conc1+2*Conc2+Conc3+2*Conc4)-(self.asZeroA1+2*self.asZeroA2+self.asZeroB1+2*self.asZeroB2))/self.asConc
		
		return Conc
	
	def cerrarSteppers(self):
			self.amMinPWM.stop()
			self,amLevPWM.stop()
		
	def leer4Concentrado(self):
		self.ahxA.select_channel(channel='A')
		Conc1 	= self.ahxA._read()
		
		self.ahxA.select_channel(channel='B')
		Conc2	= self.ahxA._read()
		
		self.ahxB.select_channel(channel='A')
		Conc3 	= self.ahxB._read()
				
		self.ahxB.select_channel(channel='B')
		Conc4	= self.ahxB._read()

		print(Conc1,"\t",Conc2,"\t",Conc3,"\t",Conc4,"\t")
		return
