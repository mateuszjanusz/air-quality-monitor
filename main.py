import sys

import wiringpi
import spidev
from numpy import median

import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085 
from mcp3008 import MCP3008
from sharpPM10 import sharpPM10
from mq import *



print('starting...')
dht_pin = 26

Adafruit_BMP085 = BMP085.BMP085()
ADC = MCP3008(0, 0) # CE0
MQ = MQ(adc=ADC, analog_channel=1)
sharpPM10 = sharpPM10(led_pin=29, pm10_pin=0, adc=ADC)




print('setup done')

while True:
    wiringpi.delay(3000) # read every 3 seconds

    # humidity, temp_dht = Adafruit_DHT.read_retry(11, dht_pin) # (sensor_type, pin_number)
    pressure = Adafruit_BMP085.read_pressure()
    temp_bmp = Adafruit_BMP085.read_temperature()
    dust_density = sharpPM10.read()
    gas = MQ.MQPercentage()

    # if humidity is not None and temperature is not None:
    #     print('\nTemp (DHT): {0:0.1f} C  Humidity: {1:0.1f} %').format(temp_dht, humidity)
    print('')
    print('Temp (BMP): {0:0.1f} C').format(temp_bmp) 
    print('Pressure: {0:0.2f} hPa').format(pressure/100)
    print('Dust density: {0:0.3f} mg/m3').format(dust_density)
    print('LPG: {0} ppm, CO: {1} ppm, Smoke: {2} ppm').format(gas['GAS_LPG'], gas['CO'], gas['SMOKE'])

