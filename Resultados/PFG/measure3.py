from hx711 import HX711
import RPi.GPIO as GPIO

try:
	hx711 = HX711(19,13,'B')

	hx711.reset()
	measure = hx711.get_raw_data_mean(30)
finally:
	GPIO.cleanup()
print("\n".join(measure))
print("Bye")
