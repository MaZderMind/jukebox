import asyncio

ROWS = 3
LEDS_PER_ROW = 21
N_LEDS = ROWS * LEDS_PER_ROW

WHITE = (1, 1, 1)
COLORS = [(0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]


class SecondaryLeds():
    def __init__(self, sender):
        self.sender = sender
        self._stopped = True

    def start(self):
        print("starting secondary LEDs")
        self._stopped = False
        asyncio.create_task(self.run())

    def stop(self):
        print("stopping secondary LEDs")
        self._stopped = True

    def idle(self):
        print("idle secondary LEDs")
        self.sender.display_frame_on_secondary_leds((WHITE,) * N_LEDS)
        self._stopped = True

    async def run(self):
        while True:
            for color in COLORS:
                if self._stopped:
                    self._stopped = False
                    print("stopped secondary LEDs")
                    return

                self.sender.display_frame_on_secondary_leds((color,) * N_LEDS)
                await asyncio.sleep(1)
