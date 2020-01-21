import socket

SHOW_STRIP0_IMMEDIATE = b'\x11'

CMD_BLACKOUT = b'\x00'


class Leds(object):
    def __init__(self, conf):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.sock.connect((conf['host'], conf['port']))

    def blackout(self):
        self.sock.send(CMD_BLACKOUT)

    def idle(self):
        self.sock.send(SHOW_STRIP0_IMMEDIATE + b'\xFF\x00\x00')

    def show(self, key_combo):
        self.sock.send(SHOW_STRIP0_IMMEDIATE + b'\x00\xFF\x00')


class LedsSimulation(object):

    def blackout(self):
        print("leds: blackout")

    def idle(self):
        print("leds: idle")

    def show(self, key_combo):
        print("leds: show", key_combo)
