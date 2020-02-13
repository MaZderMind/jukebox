import itertools
import socket

from animations.color_utils import to_byte, rgb_gamma

SHOW_STRIP0_IMMEDIATE = b'\x11'
CMD_BLACKOUT = b'\x00'


class Sender(object):
    def __init__(self, host='127.0.0.1', port=5555):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.sock.connect((host, port))

    def blackout(self):
        self.sock.send(CMD_BLACKOUT)

    def display_frame(self, frame):
        pixels = [to_byte(rgb_gamma(pixel)) for pixel in frame]
        msg = bytes(itertools.chain.from_iterable(pixels))
        self.sock.send(SHOW_STRIP0_IMMEDIATE + msg)
