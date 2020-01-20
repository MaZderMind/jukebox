#!/usr/bin/env python3
import asyncio

import evdev
import toml

from control import Control
from keys import Keys
from playback import Playback

conf = toml.load("configuration.toml")

keys = Keys()
control = Control()
playback = Playback(conf)


async def handle_keys():
    panel_name = conf['panel']['input_device_name']
    panel_devices = [
        evdev.InputDevice(dev) for dev in evdev.list_devices() if
        evdev.InputDevice(dev).name == panel_name
    ]
    if len(panel_devices) == 0:
        panel_names = [
            evdev.InputDevice(dev).name for dev in evdev.list_devices()
        ]
        print("no input-device with name", conf['panel']['input_device_name'],
              "found. The folloging devides are registered", panel_names)
        return

    panel_device = panel_devices[0]

    # noinspection PyUnresolvedReferences
    async for ev in panel_device.async_read_loop():
        print(repr(ev))


async def handle_playback_state_changes():
    while True:
        print("polling playback-state")
        await asyncio.sleep(1)


async def handle_timeout_timer():
    while True:
        print("checking for timeout")
        await asyncio.sleep(1)


async def main():
    await asyncio.wait([
        handle_keys(),
        handle_playback_state_changes(),
        handle_timeout_timer()
    ], return_when=asyncio.FIRST_COMPLETED)


if __name__ == '__main__':
    asyncio.run(main())
