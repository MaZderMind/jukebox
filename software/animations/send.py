import socket

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.connect(('jukebox', 5555))


def send(colors):
    sock.send(b'\x11' + colors)
