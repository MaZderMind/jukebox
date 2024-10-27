#!/usr/bin/env python3
import argparse
import asyncio
import signal
import sys
from datetime import datetime, timedelta

import tomllib

from control import Control, ControlSimulation
from keys import Keys
from leds import Leds, LedsSimulation
from playback import Playback
from volume import Volume


class Main(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--config", help="Path to the configuration.toml", default='./configuration.toml')
        args = parser.parse_args()

        with open(args.config, 'rb') as f:
                self.conf = conf = tomllib.load(f)

        self.keys = Keys(conf)
        self.volume = Volume(conf)
        self.control = ControlSimulation(self.keys) if conf['panel']['simulate'] else Control(self.keys)
        self.playback = Playback(conf, self.volume)
        self.leds = LedsSimulation() if conf['leds']['simulate'] else Leds(conf['leds'], conf['animations'])

        self.last_activity = datetime.now()

    async def run(self):
        self.system_on()
        await asyncio.wait([
            asyncio.create_task(self.handle_keys()),
            asyncio.create_task(self.handle_volume()),
            asyncio.create_task(self.handle_playback_state_changes()),
            asyncio.create_task(self.handle_timeout_timer()),
        ], return_when=asyncio.FIRST_COMPLETED)
        self.system_off()

    def system_on(self):
        print("system on")
        self.control.set_ready_led(True)
        self.control.set_play_led(False)
        self.control.set_solenoid(True)
        self.control.set_panel(False)
        self.leds.blackout()

    def system_off(self):
        print("system off")
        self.playback.pause()
        self.control.set_ready_led(False)
        self.control.set_play_led(False)
        self.control.set_solenoid(False)
        self.control.set_panel(False)
        self.leds.blackout()

    async def handle_keys(self):
        print("opening Panel-Input-Device")
        await self.keys.open_device()

        print("waiting for Input-Events")
        current_key_combo = None
        async for event in self.keys.wait_for_event():
            self.reset_timeout()

            if not self.control.is_panel_on():
                print("key pressed, turning panel on")
                self.control.set_panel(True)
                self.leds.idle()

            key_combo = await self.keys.get_valid_key_combo()
            if key_combo is not None:
                if current_key_combo == key_combo:
                    continue

                print("key-combo", key_combo, "detected")
                current_key_combo = key_combo

                if not self.playback.can_start(key_combo):
                    print("key-combo", key_combo, "is not playable; ejecting selection")
                    current_key_combo = None
                    await self.control.eject_solenoid()
                    continue

                print("starting playback of", key_combo)
                self.playback.start(key_combo)
                self.control.set_play_led(True)
                self.leds.show(key_combo)

            elif self.playback.is_playing():
                print("no valid key-combo detected, pausing playback")
                current_key_combo = None
                self.playback.pause()
                self.control.set_play_led(False)
                self.leds.idle()

    async def handle_volume(self):
        print("opening Volume-Input-Device")
        await self.volume.open_device()

        print("waiting for Volume-Events")
        await self.volume.handle_events()

    async def handle_playback_state_changes(self):
        was_playing = False
        while True:
            await asyncio.sleep(5)

            is_playing = self.playback.is_playing()
            if was_playing and not is_playing:
                if self.keys.any_keys_pressed():
                    print("keys still pressed but playback has stopped, ejecting")
                    self.control.set_play_led(False)
                    await self.control.eject_solenoid()
                    self.reset_timeout()
                    self.leds.idle()

            was_playing = is_playing

    async def handle_timeout_timer(self):
        while True:
            await asyncio.sleep(30)
            timeout = timedelta(minutes=self.conf['panel']['timeout_minutes'])
            is_timed_out = self.last_activity + timeout < datetime.now()

            if self.control.is_panel_on() and is_timed_out and not self.playback.is_playing():
                print("no activitiy since", self.last_activity,
                      "(over", self.conf['panel']['timeout_minutes'], "minutes), turning panel off")
                self.control.set_panel(False)
                self.control.set_play_led(False)
                self.leds.blackout()

    def reset_timeout(self):
        self.last_activity = datetime.now()


if __name__ == '__main__':
    main = Main()


    def handle_sigint(signum, stack):
        main.system_off()
        sys.exit(0)


    signal.signal(signal.SIGINT, handle_sigint)
    asyncio.run(main.run())
