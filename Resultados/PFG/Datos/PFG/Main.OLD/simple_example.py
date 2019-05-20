#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711

GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
try:
	while True:
		
		hxA = HX711(dout_pin=11, pd_sck_pin=9, gain_channel_A=128, select_channel='B')  # create an object
		hxB = HX711(dout_pin=11, pd_sck_pin=9, gain_channel_A=128, select_channel='A')
		val1 = hxA.get_raw_data_mean(readings=1)
		val2 = hxB.get_raw_data_mean(readings=1)
		print("%d\t%d\n"%(val1,val2))

finally:
	GPIO.cleanup()
