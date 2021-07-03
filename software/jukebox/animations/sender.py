import itertools
import socket

from animations.color_utils import to_byte, rgb_gamma

SHOW_STRIP_IMMEDIATE = 0x11
CMD_BLACKOUT = b'\x00'


class Sender(object):
    def __init__(self, host='127.0.0.1', port=5555):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        self.sock.connect((host, port))

    def blackout(self):
        self.sock.send(CMD_BLACKOUT)

    def display_frame(self, frame, strip_index=0):
        msg = self._frame_to_msg(frame)
        command = SHOW_STRIP_IMMEDIATE + strip_index
        self.sock.send(command.to_bytes(1, 'big') + msg)

    def display_frame_on_secondary_leds(self, frame):
        self.display_frame(frame, 1)

    def _frame_to_msg(self, frame):
        pixels = [to_byte(rgb_gamma(pixel)) for pixel in frame]
        msg = bytes(itertools.chain.from_iterable(pixels))
        return msg
