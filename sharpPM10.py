import wiringpi

class sharpPM10:
    def __init__(self, led_pin, pm10_pin, adc, sampling_time=280, delta_time=40, sleep_time=9680):
        if led_pin is None:
            raise ValueError('led pin number is missing!')
        if pm10_pin is None:
            raise ValueError('pm10 pin number is missing!')

        if not adc:
            from mcp3008 import MCP3008
            self.adc = MCP3008()
        else:
            self.adc = adc

        self.led_pin = led_pin
        self.pm10_pin = pm10_pin
        
        wiringpi.wiringPiSetupGpio() 
        wiringpi.pinMode(led_pin, 1)
        wiringpi.digitalWrite(led_pin, 0)

        self.sampling_time = sampling_time
        self.delta_time = delta_time
        self.sleep_time = sleep_time

    
    def read(self):
        wiringpi.digitalWrite(self.led_pin, 1) # power on the LED
        wiringpi.delayMicroseconds(self.sampling_time) 
        wiringpi.delayMicroseconds(self.delta_time)
        vo_measured = self.adc.read(self.pm10_pin) # read the dust value
        wiringpi.digitalWrite(self.led_pin, 0) # turn the LED off

        # Voltage 0 - 5V mapped to 0 - 1023 integer values
        calc_voltage = vo_measured * (5.0 / 1024)
        
        # linear eqaution taken from http://www.howmuchsnow.com/arduino/airquality/ (Chris Nafis (c) 2012)
        dust_density = 0.17 * calc_voltage - 0.1

        return dust_density
        
    
    def readSequence(self):
        vo_measured = 0
        readings = []

        for i in range(10):
            wiringpi.digitalWrite(self.led_pin, 1) # power on the LED
            wiringpi.delayMicroseconds(self.sampling_time) 
            wiringpi.delayMicroseconds(self.delta_time)
            vo_measured = self.adc.read(self.pm10_pin) # read the dust value
            wiringpi.digitalWrite(self.led_pin, 0) # turn the LED off

            wiringpi.delayMicroseconds(self.sleep_time) # wait 9.68ms before the next sequence is repeated

            # Voltage 0 - 5V mapped to 0 - 1023 integer values
            calc_voltage = vo_measured * (5.0 / 1024)
            
            # linear eqaution taken from http://www.howmuchsnow.com/arduino/airquality/ (Chris Nafis (c) 2012)
            dust_density = 0.17 * calc_voltage - 0.1
            readings.append(dust_density)

        return median(readings)