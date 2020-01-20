import socket

SHOW_STRIP0_IMMEDIATE = b'\x11'

CMD_BLACKOUT = b'\x00'

LED_SERVER_IP = "::1"
LED_SERVER_PORT = 5555


class Leds(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.sock.connect((LED_SERVER_IP, LED_SERVER_PORT))

    def blackout(self):
        self.sock.send(CMD_BLACKOUT)

    def idle(self):
        self.sock.send(SHOW_STRIP0_IMMEDIATE + b'\xFF\x00\x00')

    def show(self, key_combo):
        self.sock.send(SHOW_STRIP0_IMMEDIATE + b'\x00\xFF\x00')
