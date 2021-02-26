from datetime import datetime
import spidev
import RPi.GPIO as GPIO
from time import sleep

def printbits(data, padding=8):
    template = '{{:0{}b}}'.format(padding)
    for d in data:
        print(template.format(d))

def spisetup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT)
    #sleep(0.8)
    spi = spidev.SpiDev()
    #GPIO.output(21, GPIO.HIGH)
    spi.open(0, 1)
    #spi.no_cs = False
    spi.no_cs = True
    GPIO.output(21, GPIO.HIGH)

    spi.max_speed_hz = 1000000
    spi.bits_per_word = 8
    spi.mode = 1

    GPIO.output(21, GPIO.LOW)
    spi.xfer([0x80, 0b00010010])             # write configuration
    GPIO.output(21, GPIO.HIGH)
    #printbits(spi.xfer([0x00, 0x00])[1:])   # read configuration
    return spi

def spiread(spi, r_ref=430):
    GPIO.output(21, GPIO.LOW)
    spi.xfer([0x80, 0b10010010])             # v-bias on
    GPIO.output(21, GPIO.HIGH)
    sleep(0.1)                               # wait for RTDIN-capacitor full
    GPIO.output(21, GPIO.LOW)
    spi.xfer([0x80, 0b10110010])             # start 1-shot reading
    GPIO.output(21, GPIO.HIGH)
    sleep(0.1)                               # wait for saving to register
    GPIO.output(21, GPIO.LOW)
    bits = spi.xfer([0x01, 0x00, 0x00])[1:]  # read bits
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(21, GPIO.LOW)
    spi.xfer([0x80, 0b00010010])             # v-bias off
    GPIO.output(21, GPIO.HIGH)
    adc = bits[0] << 7 | bits[1] >> 1        # make 15 bits
    #printbits(bits)
    #printbits([adc], padding=15)
    r_rtd = 1.0* (adc * r_ref) / 2 ** 15 
    #print('r_rtd:{}ohm'.format(r_rtd))
    adc = adc * r_ref / 400                  # convert adc on r_ref == 400
    temperature = adc / 32 - 256             # convert adc to temperature
    return r_rtd

def spiquit(spi):
    spi.close()
    GPIO.cleanup()


if __name__ == '__main__':
    #try:
    spi = spisetup()
    #while True:
    tempareture = spiread(spi)
    print('{:%Y-%m-%d %H:%M:%S} ohm {:5.5f}'.format(
        datetime.now(), tempareture))
    #sleep(1)
    #except KeyboardInterrupt:
    spiquit(spi)
    exit(0)
