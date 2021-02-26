from datetime import datetime
import spidev
from time import sleep

def printbits(data, padding=8):
    template = '{{:0{}b}}'.format(padding)
    for d in data:
        print(template.format(d))

def spisetup():
    spi = spidev.SpiDev()
    spi.open(0, 1)
    spi.max_speed_hz = 1000000
    spi.bits_per_word = 8
    spi.mode = 1
    spi.xfer([0x80, 0b00010010])             # write configuration
    #printbits(spi.xfer([0x00, 0x00])[1:])   # read configuration
    return spi

def spiread(spi, r_ref=430):
    spi.xfer([0x80, 0b10010010])             # v-bias on
    sleep(0.1)                               # wait for RTDIN-capacitor full
    spi.xfer([0x80, 0b10110010])             # start 1-shot reading
    sleep(0.1)                               # wait for saving to register
    bits = spi.xfer([0x01, 0x00, 0x00])[1:]  # read bits
    spi.xfer([0x80, 0b00010010])             # v-bias off
    adc = bits[0] << 7 | bits[1] >> 1        # make 15 bits
    #printbits(bits)
    #printbits([adc], padding=15)
    r_rtd = (adc * r_ref) / 2 ** 15
    #print('r_rtd:{}ohm'.format(r_rtd))
    adc0 = adc
    adc = adc * r_ref / 400                  # convert adc on r_ref == 400
    temperature = adc / 32 - 256             # convert adc to temperature
    return adc0

def spiquit(spi):
    spi.close()


if __name__ == '__main__':
    try:
        spi = spisetup()
        while True:
            tempareture = spiread(spi)
            print('{:%Y-%m-%d %H:%M:%S} adc {:5.0f}'.format(
                datetime.now(), tempareture))
            sleep(1)
    except KeyboardInterrupt:
        spiquit(spi)
        exit(0)
