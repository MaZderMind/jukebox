#!/usr/bin/env python3
import socket
from typing import Optional

from rpi_ws281x import PixelStrip

UDP_IP = "::"
UDP_PORT = 5555

STRIP_0 = {
    "LED_COUNT": 15 * 11,
    "PIN": 12
}
STRIP_1 = {
    "LED_COUNT": 10,
    "PIN": 13
}

LED_FREQ_HZ = 800_000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)

strip0: Optional[PixelStrip] = None
strip1: Optional[PixelStrip] = None


def black_out():
    for i in range(0, strip0.numPixels()):
        strip0.setPixelColor(i, 0)

    for i in range(0, strip1.numPixels()):
        strip1.setPixelColor(i, 0)


def set_pixels(led_strip_index, colors):
    strip = strip0 if led_strip_index == 0 else strip1
    for i in range(0, strip.numPixels()):
        offset = i * 3
        if len(colors) > offset + 2:
            strip.setPixelColorRGB(i, colors[offset + 0], colors[offset + 1], colors[offset + 2])
        else:
            strip.setPixelColor(i, 0)


def show():
    strip0.show()
    strip1.show()


def set_brightness(brightness):
    print("set_brightness", brightness)
    strip0.setBrightness(brightness)
    strip1.setBrightness(brightness)


def main():
    global strip0, strip1

    print("Listing to Datagrams on", UDP_IP, UDP_PORT)
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    strip0 = PixelStrip(STRIP_0["LED_COUNT"], STRIP_0["PIN"], LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, 0)
    strip1 = PixelStrip(STRIP_1["LED_COUNT"], STRIP_1["PIN"], LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, 1)

    strip0.begin()
    strip1.begin()

    while True:
        data, addr = sock.recvfrom(5000)

        command = data[0]
        if command == 0x00:  # Black Out
            black_out()
            show()
        elif command in [0x01, 0x02]:  # Set Colors
            led_strip_index = command - 0x01
            set_pixels(led_strip_index, data[1:])
        elif command in [0x11, 0x12]:  # Set Colors Immediate
            led_strip_index = command - 0x11
            set_pixels(led_strip_index, data[1:])
            show()
        elif command == 0x40:  # Set Brightness
            set_brightness(data[1])
            show()
        elif command == 0xFF:  # Show
            show()


if __name__ == '__main__':
    main()
