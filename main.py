import machine
import network
import socket

from ssd1306 import SSD1306_I2C

""" Constants """
WIDTH = const(64)
HEIGHT = const(48)
pscl = machine.Pin(5)  # GPIO4_CLK , machine.Pin.OUT_PP)
psda = machine.Pin(4)  # GPIO5_DAT, machine.Pin.OUT_PP)
i2c = machine.I2C(scl=pscl, sda=psda)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
#writer = Writer(oled, font)
# This is ugly classmethod
#Writer.set_clip(True, True)


class ApouiControl:
    """ 
    This has to be used to a shell class of sort
    This is just a temporary namespace
    """
    relayurl = 'http://control.maison.apoui.net/setrelay'

    @classmethod
    def relay_on(self, relay):
        url = '{0}/on/{1}'.format(self.relayurl, relay)
        self._http_get(url)

    @classmethod
    def relay_off(self, relay):
        url = '{0}/off/{1}'.format(self.relayurl, relay)
        self._http_get(url)

    def _http_get(self, url):
        _, _, host, path = url.split('/', 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.1\r\nHost: %s\r\n\r\n' %
                     (path, host), 'utf8'))
        while True:
            data = s.recv(100)
            if data:
                print(str(data, 'utf8'), end='')
            else:
                break


class MicroWifi:
    """Connector to the Wifi"""

    def __init__(self, ssid, key):
        self.ssid = ssid
        self.key = key
        self.do_connect(self.ssid, self.key)

    def do_connect(self, ssid, key):
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            oled.text('>WIFI:', 0, 10)
            oled.show()
            sta_if.active(True)
            sta_if.connect(ssid, key)
            while not sta_if.isconnected():
                pass
        oled.text('OK', 7, 10)
        oled.show()


def main():
    oled.text(">KERNEL", 0, 0)
    oled.show()
    # We should have a list of wifi we can try to connect to ?
    #[i for i, v in enumerate(network.WLAN(network.STA_IF).scan()) if v[0] == 'excellency']
    wifi = MicroWifi.do_connect(
        'APOUI', 'astis4-maledictio6-pultarius-summittite')

main()
