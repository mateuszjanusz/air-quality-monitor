import sys

import wiringpi
import spidev
from numpy import median
import wiringpi
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085 
from mcp3008 import MCP3008
from sharpPM10 import sharpPM10
from mq import *

import MySQLdb
import config

print('starting...')

dht_pin = 19
sharp_pin = 21
sharp_channel = 0
mq_channel = 1

green_led = 6
yellow_led = 13

try:
    wiringpi.wiringPiSetupGpio() 
    wiringpi.pinMode(green_led, 1)
    wiringpi.pinMode(yellow_led, 1)

    wiringpi.digitalWrite(yellow_led, 1) # power on the yellow LED
    wiringpi.digitalWrite(green_led, 1) # power on the green LED

    Adafruit_BMP085 = BMP085.BMP085()
    ADC = MCP3008(0, 0) # CE0
    MQ = MQ(adc=ADC, analog_channel=mq_channel)
    sharpPM10 = sharpPM10(led_pin=sharp_pin, pm10_pin=sharp_channel, adc=ADC)
except:
    wiringpi.digitalWrite(green_led, 0) # power off the green LED

while True:
    wiringpi.digitalWrite(yellow_led, 1) # power on the yellow LED

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
        wiringpi.digitalWrite(yellow_led, 0) # power off the yellow LED
    except:
        db.rollback()
        print('failed!')
        wiringpi.digitalWrite(green_led, 0) # power off the green LED


    db.close()
    print('connection closed')
    time.sleep(1800) #900sec = 15min

##    if humidity is not None and temperature is not None:
##    print('\nTemp (DHT): {0:0.1f} C  Humidity: {1:0.1f} %').format(temp_dht, humidity)
##    print('Temp (BMP): {0:0.1f} C').format(temp_bmp) 
##    print('Pressure: {0:0.2f} hPa').format(pressure/100)
##    print('Dust density: {0:0.3f} mg/m3').format(dust_density)
##    print('LPG: {0} ppm, CO: {1} ppm, Smoke: {2} ppm').format(gas['GAS_LPG'], gas['CO'], gas['SMOKE'])





