#!/usr/bin/env python3
import asyncio
import signal
from datetime import datetime

import toml

from control import Control
from keys import Keys
from leds import Leds
from playback import Playback


class Main(object):
    def __init__(self):
        conf = toml.load("configuration.toml")

        self.keys = Keys(conf['panel'])
        self.control = Control()
        self.playback = Playback(conf)
        self.leds = Leds()

        self.last_activity = datetime.now()

    async def run(self):
        self.system_on()
        await asyncio.wait([
            self.handle_keys(),
            self.handle_playback_state_changes(),
            self.handle_timeout_timer()
        ], return_when=asyncio.FIRST_COMPLETED)
        self.system_off()

    def system_on(self):
        self.control.set_ready_led(True)
        self.control.set_play_led(False)
        self.control.set_solenoid(False)
        self.control.set_panel(False)
        self.leds.blackout()

    def system_off(self):
        self.control.set_ready_led(False)
        self.control.set_play_led(False)
        self.control.set_solenoid(False)
        self.control.set_panel(False)
        self.leds.blackout()

    async def handle_keys(self):
        print("opening Panel-Input-Device")
        await self.keys.open_device()

        async for valid_key_combo in self.keys.wait_for_event():
            self.reset_timeout()
            if not self.control.is_panel_on():
                print("key pressed, turning panel on")
                self.control.set_panel(True)
                self.leds.idle()

            if valid_key_combo is not None:
                print("valid key-combo", valid_key_combo, "detected, starting playback")
                self.playback.start(valid_key_combo)
                self.leds.show(valid_key_combo)

            elif self.playback.is_playing():
                print("no valid key-combo detected, pausing playback")
                self.playback.pause()
                self.leds.idle()

    def reset_timeout(self):
        # print("resetting timeout")
        self.last_activity = datetime.now()

    async def handle_playback_state_changes(self):
        while True:
            # print("polling playback-state")
            await asyncio.sleep(1)

    async def handle_timeout_timer(self):
        while True:
            # print("checking for timeout")
            await asyncio.sleep(1)


if __name__ == '__main__':
    main = Main()
    signal.signal(signal.SIGINT, main.system_off)
    asyncio.run(main.run())
