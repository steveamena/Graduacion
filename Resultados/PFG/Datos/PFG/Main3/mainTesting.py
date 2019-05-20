#Funcion para probar funciones antes de agregarlas al programa principal
#15/05/19
#Steve Alberto Mena Navarro
#GC@2019

from cowlist import Cowlist
from dosificadora import Dosificadora
UberCow = Dosificadora()

print(dato)
input("Digite cualquier tecla")

listaVacas = Cowlist(59,3)
nombreArchivo = listaVacas.get_name_from_Interface()
listaVacas.loadData(nombreArchivo)
vaca = input("Digite el numero de vaca ")
racion = listaVacas.get_cow_ration(vaca)
print(racion[0],racion[1],racion[2])
