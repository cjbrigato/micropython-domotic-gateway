import machine
import network
import socket

from cmd import Cmd

from ssd1306 import SSD1306_I2C

""" Constants """
WIDTH = const(64)
HEIGHT = const(48)
pscl = machine.Pin(5)  # GPIO4_CLK , machine.Pin.OUT_PP)
psda = machine.Pin(4)  # GPIO5_DAT, machine.Pin.OUT_PP)
i2c = machine.I2C(scl=pscl, sda=psda)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)


class ApouiShell(Cmd):

    def __init__(self,  controller):
        super().__init__()
        self.controller = controller

    def do_relay_off(self, args):
        if len(args) == 0:
            print("<< Relay id ?")
        elif len(args) == 1:
            relay = args
            self.controller.relay_off(relay)
            print(">> Shut Relay {0} Down".format(relay))
        else:
            print("<< Ambigous : {0}".format(args))

    def do_relay_on(self, args):
        if len(args) == 0:
            print("<< Relay id ?")
        elif len(args) == 1:
            relay = args
            self.controller.relay_on(relay)
            print(">> Lighted Relay {0} Up".format(relay))
        else:
            print("<< Ambigous : {0}".format(args))

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        machine.reset()


class ApouiControl:
    """ 
    This is firt Domotic Controller
    This has to be used to a shell class of sort
    """

    def __init__(self, relayurl):
        self.relayurl = relayurl
        self._boot_tests('1')

    def relay_on(self, relay):
        url = '{0}/{1}/on'.format(self.relayurl, relay)
        self._http_get(url)

    def relay_off(self, relay):
        url = '{0}/{1}/off'.format(self.relayurl, relay)
        self._http_get(url)

    def _http_get(self, url):
        _, _, host, path = url.split('/', 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.1\r\nHost: %s\r\n\r\n' %
                     (path, host), 'utf8'))
        """ Tempory buh
        while True:
            data = s.recv(8192)
            if data:
                print(str(data, 'utf8'), end='')
            else:
                break
        """
        s.close()

    def _boot_tests(self, relay):
        self.relay_off(relay)
        self.relay_on(relay)


class MicroWifi:
    """Connector to the Wifi"""

    def __init__(self, ssid, key):
        self.ssid = ssid
        self.key = key
        self._do_connect(self.ssid, self.key)

    def _do_connect(self, ssid, key):
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            oled.text('>WIFI:', 0, 20)
            oled.show()
            sta_if.active(True)
            sta_if.connect(ssid, key)
            while not sta_if.isconnected():
                pass
        oled.text('OK', 48, 20,)
        oled.show()


def boot(productstate):
    oled.text("->KERNEL", 0, 0)
    oled.show()
    oled.text(productstate, 0, 10)
    oled.show()
    # We should have a list of wifi we can try to connect to ?
    #[i for i, v in enumerate(network.WLAN(network.STA_IF).scan()) if v[0] == 'excellency']
    wifi = MicroWifi('APOUI', 'astis4-maledictio6-pultarius-summittite')
    controller = ApouiControl('http://control.maison.apoui.net/setrelay')
    oled.text('>TESTS:1', 0, 30)
    oled.show()
    oled.text(" [READY]", 0, 40)
    oled.show()
    return controller


def main():
    controller = boot('>V:A0B')
    shell = ApouiShell(controller)
    shell.prompt = 'apoui@hc> '
    shell.cmdloop('Ready. Spawning ApouiShell')

main()
