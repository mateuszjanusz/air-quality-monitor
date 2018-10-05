from spidev import SpiDev

class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()

    def open(self):
        self.spi.open(self.bus, self.device)
    
    def read(self, adc_channel = 0):
        # 0-7 channels available only
        if ((adc_channel > 7) or (adc_channel < 0)):
            return -1
        r = self.spi.xfer2([1, (8 + adc_channel) << 4, 0])
        adc_output = ((r[1] & 3) << 8) + r[2]
        return adc_output
            
    def close(self):
        self.spi.close()