import asyncio

ROWS = 3
LEDS_PER_ROW = 21
N_LEDS = ROWS * LEDS_PER_ROW

WHITE = (1, 1, 1)
COLORS = [(0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]


class SecondaryLeds():
    def __init__(self, sender):
        self.sender = sender
        self._stopped = False

    def start(self):
        print("Starting secondary LEDs")
        asyncio.create_task(self.run())

    def stop(self):
        print("Stopping secondary LEDs")
        self._stopped = True

    def idle(self):
        print("Idle secondary LEDs")
        self.sender.display_frame_on_secondary_leds(WHITE * N_LEDS)
        pass

    async def run(self):
        while True:
            for color in COLORS:
                self.sender.display_frame_on_secondary_leds(color * N_LEDS)
                await asyncio.sleep(1)

                if self._stopped:
                    print("Stopped secondary LEDs")
                    return
