import asyncio

ROWS = 3
LEDS_PER_ROW = 21
N_LEDS = ROWS * LEDS_PER_ROW

WHITE = (1, 1, 1)
COLORS = [(0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]


class SecondaryLeds():
    def __init__(self, sender):
        self.sender = sender
        self._task = None

    def start(self):
        self.stop()

        print("starting secondary LEDs")
        self._task = asyncio.create_task(self.run())

    def stop(self):
        if self._task is not None:
            print("stopping secondary LEDs")
            self._task.cancel()
            self._task = None

    def idle(self):
        print("idle secondary LEDs")
        self.sender.display_frame_on_secondary_leds((WHITE,) * N_LEDS)

    async def run(self):
        while True:
            for color in COLORS:
                self.sender.display_frame_on_secondary_leds((color,) * N_LEDS)
                await asyncio.sleep(1)
