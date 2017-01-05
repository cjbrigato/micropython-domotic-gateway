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
import scpl11
writer = Writer(ssd, scpl11)

#[i for i, v in enumerate(network.WLAN(network.STA_IF).scan()) if v[0] == 'excellency']

relay1off = 'http://control.maison.apoui.net/setrelay/1/off'
relay1on = 'http://control.maison.apoui.net/setrelay/1/on'

def do_connect(ssid,key):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        writer.printstring('Wifi..')
        ssd.show()
        sta_if.active(True)
        sta_if.connect(ssid, key)
        while not sta_if.isconnected():
            pass
    writer.printstring('OK\n')
    ssd.show()
    writer.printstring('Ready\n')
    ssd.show()

def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.1\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break

relayurl='http://control.maison.apoui.net/setrelay'

def relay_on(relay):
	url='{0}/on/{1}'.format(relayurl,relay)
	http_get(url)

def relay_off(relay):
	url='{0}/off/{1}'.format(relayurl,relay)
	http_get(url)

Writer.set_clip(True, True)
writer.printstring('Booting..OK\n')
ssd.show()
do_connect('APOUI', 'astis4-maledictio6-pultarius-summittite')