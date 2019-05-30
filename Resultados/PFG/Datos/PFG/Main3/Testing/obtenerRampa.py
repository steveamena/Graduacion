import RPi.GPIO as GPIO
from dosificadora import Dosificadora

#iniciar GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Rampa = Dosificadora()
Rampa.obtenerFuncionRampaTR(99)
