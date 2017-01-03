# ssd1306_test.py Demo pogram for rendering arbitrary fonts to an SSD1306
# OLED display

# https://learn.adafruit.com/monochrome-oled-breakouts/wiring-128x32-spi-oled-display
# https://www.proto-pic.co.uk/monochrome-128x32-oled-graphic-display.html

# V0.2 Dec 17th 2016 Now supports updated framebuf module.

import network
import socket
import machine

from ssd1306 import SSD1306_I2C
WIDTH = const(64)
HEIGHT = const(48)
pscl = machine.Pin(5)  # GPIO4_CLK , machine.Pin.OUT_PP)
psda = machine.Pin(4)  # GPIO5_DAT, machine.Pin.OUT_PP)
i2c = machine.I2C(scl=pscl, sda=psda)
ssd = SSD1306_I2C(WIDTH, HEIGHT, i2c)

from writer import Writer
# Fonts
#import freesans20
#import freeserif19
#import inconsolata14
import scpl11
writer = Writer(ssd, scpl11)

#[i for i, v in enumerate(network.WLAN(network.STA_IF).scan()) if v[0] == 'excellency']
#if enumerate(network.WLAN(network.STA_IF).scan()) == 'excellency':
#	writer.printstring('hey!')
#else:
#	writer.printstring('hoy!')


def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break

def do_connect(ssid,key):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        writer.printstring('Wifi...\n')
        ssd.show()
        sta_if.active(True)
        sta_if.connect(ssid, key)
        while not sta_if.isconnected():
            pass
    writer.printstring('OK :)')
    ssd.show()


Writer.set_clip(True, True)
writer.printstring('Booting...\n')
ssd.show()
# if [i for i, v in enumerate(network.WLAN(network.STA_IF).scan()) if v[0] == 'excellency']
do_connect('excellency', 'independenceday')

addr_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)
addr = addr_info[0][-1]
s = socket.socket()
s.connect(addr)
while True:
    data = s.recv(500)
    print(str(data, 'utf8'), end='')