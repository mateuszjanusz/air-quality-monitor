import sys

import wiringpi
import spidev
from numpy import median

import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085 
from mcp3008 import MCP3008
from sharpPM10 import sharpPM10
from mq import *

import MySQLdb
import config

print('starting...')
dht_pin = 19

Adafruit_BMP085 = BMP085.BMP085()
ADC = MCP3008(0, 0) # CE0
MQ = MQ(adc=ADC, analog_channel=1)
sharpPM10 = sharpPM10(led_pin=29, pm10_pin=0, adc=ADC)
 


while True:
    humidity, temp_dht = Adafruit_DHT.read_retry(11, dht_pin) # (sensor_type, pin_number)
    pressure = Adafruit_BMP085.read_pressure()
    temp_bmp = Adafruit_BMP085.read_temperature()
    dust_density = sharpPM10.read()
    gas = MQ.MQPercentage()
    
    db = MySQLdb.connect(config.host, config.user, config.password, config.db_name)
    print('connected')

    cursor = db.cursor()
    
    sql = ("INSERT INTO readings (temp, humidity, pressure, dust, lpg, co, smoke)\
            VALUES ({0:0.1f},{1:0.1f},{2:0.2f},{3:0.3f},{4:0.4f},{5:0.4f},{6:0.4f})").format(
            temp_bmp, humidity, pressure/100, dust_density, gas['GAS_LPG'], gas['CO'], gas['SMOKE'])

    try:
        cursor.execute(sql)
        db.commit()
        print('success')
    except:
        db.rollback()
        print('failed')

    db.close()
    print('connection closed')
    time.sleep(900) #900sec = 15min

##    if humidity is not None and temperature is not None:
##    print('\nTemp (DHT): {0:0.1f} C  Humidity: {1:0.1f} %').format(temp_dht, humidity)
##    print('Temp (BMP): {0:0.1f} C').format(temp_bmp) 
##    print('Pressure: {0:0.2f} hPa').format(pressure/100)
##    print('Dust density: {0:0.3f} mg/m3').format(dust_density)
##    print('LPG: {0} ppm, CO: {1} ppm, Smoke: {2} ppm').format(gas['GAS_LPG'], gas['CO'], gas['SMOKE'])

