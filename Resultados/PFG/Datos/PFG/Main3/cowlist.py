##Definicion de clase dosificadora
##Steve Mena Navarro
## 15 Mayo 2019
## 2019 @ GanaCenter

#Importaciones
import numpy as np		#Libreria de manejo de listas
import openpyxl as xl	#Libreria de acceso de archivos de Excel
from tkinter import filedialog
from tkinter import *

class Cowlist:
	def __init__(self,filas,columnas):
		#inicializa todos los parametros de la clase cowlist
			self.listaVacas = np.zeros((filas,columnas),np.float32)
			
	def __del__(self):
		#Elimina cualquier rastro y destruye los objetos de la clase cowlist
		nombre = self.__class__.__name__
		print(nombre, "Destruido")
		
	def loadData(self,nombreExcel = ""):
		#Carga los datos desde el archivo de Excel
		print("Cargando el archivo de balances")
		book = xl.load_workbook(nombreExcel)		#Obtener libro excel
		sheet = book.get_sheet_by_name('L1')	#Obtener hoja excel
		multiple_cells = [sheet['C6':'C64'],sheet['H6':'H64'],sheet['K6':'K64']]
		
		i = 0
		#Obtener numeros de vaca
		for col in multiple_cells:
			j = 0
			for cell in col:				
				self.listaVacas[j,i] = cell[0].value
				j += 1
			i += 1
		print("Balances Cargados")
		
	def get_name_from_Interface(self):
		root = Tk()
		root.filename = filedialog.askopenfilename(initialdir = "/home/pi/Desktop/PFG/Main2",title = "Seleccionar archivo",
		filetypes = (("Archivos Excel",".xlsx"),("Todos los archivos","*.")))
		self.nombreExcel = root.filename
		print("Direccion obtenida")
		root.destroy()
		return root.filename
	
	def get_cow_ration(self,cowNumber):
		index = np.where(self.listaVacas[:,0]==int(cowNumber))[0][0]	
		return (self.listaVacas[index,0],self.listaVacas[index,1],self.listaVacas[index,2])
