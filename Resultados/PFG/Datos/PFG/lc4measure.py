#Script usado para cuando se probaron las cuatro celdas de carga de la tolva 
#romana inicialmente.
#Nota: Funciona solamente si hay un amplificador por celda de carga.
#Python 2.7.x
#29/05/2019: Documentados detalles importantes

import RPi.GPIO as GPIO
import time
import sys
import math
from hx711 import HX711

def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()

#GPIO.setwarnings(False)
#Inicializar las celdas de carga
#GPIO.cleanup()

lc1 = HX711(5,6)
lc2 = HX711(13,19)
lc3 = HX711(17,27)
lc4 = HX711(20,21)

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
lc1.set_reading_format("LSB", "MSB")
lc2.set_reading_format("LSB","MSB")
lc3.set_reading_format("LSB","MSB")
lc4.set_reading_format("LSB","MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
unit = 53043.282
lc1.set_reference_unit(unit)
lc2.set_reference_unit(unit)
lc3.set_reference_unit(unit)
lc4.set_reference_unit(unit)
#hx.set_reference_unit()

#tarar las celdas de carga
lc1.reset()
lc1.tare()
lc2.reset()
lc2.tare()
lc3.reset()
lc3.tare()
lc4.reset()
lc4.tare()

val_ant = 0
offset = 0
offset_ant = 0
try:
    while True:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment the three lines to see what it prints.
        #np_arr8_string = hx.get_np_arr8_string()
        #binary_string = hx.get_binary_string()
        #print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val1 = lc1.get_weight(2)
	val2 = lc2.get_weight(2)
	val3 = lc3.get_weight(3)
	val4 = lc4.get_weight(4)
	
	val = (val1+val2+val3+val4)/4
#	print(val)
#	if(abs(val)<=4):
#		offset = (val+offset_ant)/2
#		val =  offset
#	else:
#		offset = 0
 #       val = val-offset
#	val = (val_ant+va#l)/2
#	print (int(math.floor(val)))
	print(val)
	#print (offset)
	offset_ant = offset
	val_ant = val

       # hx.power_down()
       # hx.power_up()
       # time.sleep(0.1)
except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
finally:
        GPIO.cleanup()
        
