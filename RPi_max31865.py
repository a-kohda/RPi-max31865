# coding: utf-8
from datetime import datetime
import spidev
import RPi.GPIO as GPIO
from time import sleep
import sys

CS_list = [19,20,21]     # 使用するすべてのCSピンリスト
abcs=int(sys.argv[1])    # 今使うCSピン(コマンドライン引数)

def spisetup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CS_list, GPIO.OUT)
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.no_cs = True    # spidevによるCSピンの自動制御を無効化
    GPIO.output(CS_list, GPIO.HIGH)
    spi.max_speed_hz = 1000000   # 1 MHz
    spi.bits_per_word = 8
    spi.mode = 1
    GPIO.output(abcs, GPIO.LOW)
    spi.xfer([0x80, 0b00010010])             # write configuration
    GPIO.output(abcs, GPIO.HIGH)
    return spi

def spiread(spi, r_ref=430):
    GPIO.output(abcs, GPIO.LOW)
    spi.xfer([0x80, 0b10010010])             # v-bias on
    GPIO.output(abcs, GPIO.HIGH)
    sleep(0.1)                               # wait for RTDIN-capacitor full
    GPIO.output(abcs, GPIO.LOW)
    spi.xfer([0x80, 0b10110010])             # start 1-shot reading
    GPIO.output(abcs, GPIO.HIGH)
    sleep(0.1)                               # wait for saving to register
    GPIO.output(abcs, GPIO.LOW)
    bits = spi.xfer([0x01, 0x00, 0x00])[1:]  # read bits
    GPIO.output(abcs, GPIO.HIGH)
    GPIO.output(abcs, GPIO.LOW)
    spi.xfer([0x80, 0b00010010])             # v-bias off
    GPIO.output(abcs, GPIO.HIGH)
    adc = bits[0] << 7 | bits[1] >> 1        # make 15 bits
    r_rtd = 1.0* (adc * r_ref) / 2 ** 15 
    return r_rtd

def spiquit(spi):
    spi.close()
    GPIO.cleanup()

if __name__ == '__main__':
    spi = spisetup()
    ohm = spiread(spi)
    print('%.2f' % ohm)
    spiquit(spi)
    exit(0)
