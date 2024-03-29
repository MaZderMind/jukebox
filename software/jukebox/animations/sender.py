import itertools
import socket

from animations.color_utils import to_byte, rgb_gamma

SHOW_STRIP_IMMEDIATE = 0x11
CMD_BLACKOUT = b'\x00'


class Sender(object):
    def __init__(self, host='127.0.0.1', port=5555, strip_index=0):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((host, port))
        self.strip_index = strip_index

    def blackout(self):
        self._send(CMD_BLACKOUT)

    def display_frame(self, frame):
        msg = self._frame_to_msg(frame)
        command = SHOW_STRIP_IMMEDIATE + self.strip_index
        self._send(command.to_bytes(1, 'big') + msg)

    def _send(self, data):
        try:
            self.sock.send(data)
        except ConnectionRefusedError:
            pass

    def display_frame_on_secondary_leds(self, frame):
        self.display_frame(frame)

    def _frame_to_msg(self, frame):
        pixels = [to_byte(rgb_gamma(pixel)) for pixel in frame]
        msg = bytes(itertools.chain.from_iterable(pixels))
        return msg
