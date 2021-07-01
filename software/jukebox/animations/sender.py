import itertools
import socket

from animations.color_utils import to_byte, rgb_gamma

SHOW_STRIP0_IMMEDIATE = b'\x11'
SHOW_STRIP1_IMMEDIATE = b'\x12'
CMD_BLACKOUT = b'\x00'


class Sender(object):
    def __init__(self, host='127.0.0.1', port=5555):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((host, port))

    def blackout(self):
        self.sock.send(CMD_BLACKOUT)

    def display_frame(self, frame):
        msg = self._frame_to_msg(frame)
        self.sock.send(SHOW_STRIP0_IMMEDIATE + msg)

    def display_frame_on_secondary_leds(self, frame):
        msg = self._frame_to_msg(frame)
        self.sock.send(SHOW_STRIP1_IMMEDIATE + msg)

    def _frame_to_msg(self, frame):
        pixels = [to_byte(rgb_gamma(pixel)) for pixel in frame]
        msg = bytes(itertools.chain.from_iterable(pixels))
        return msg
