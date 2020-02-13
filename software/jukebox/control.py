import asyncio


def _read(led):
    with open("/sys/class/leds/" + led + "/brightness", 'r') as io:
        r = io.read().strip()
        return r != "0"


def _write(led, onoff):
    with open("/sys/class/leds/" + led + "/brightness", 'w') as io:
        io.write("255" if onoff else "0")


def _write_blinking(led, onoff):
    with open("/sys/class/leds/" + led + "/trigger", 'w') as io:
        io.write("timer" if onoff else "none")


class Control(object):
    def __init__(self, keys):
        self.keys = keys

    def set_ready_led(self, onoff):
        _write('led_ready', onoff)

    def set_play_led(self, onoff):
        _write_blinking('led_play', onoff)

    def set_solenoid(self, onoff):
        _write('solenoid', onoff)

    def is_solenoid_on(self):
        return _read('solenoid')

    async def eject_solenoid(self):
        if self.is_solenoid_on():
            self.set_solenoid(False)
            while self.keys.any_keys_pressed():
                await asyncio.sleep(0.25)
            self.set_solenoid(True)

    def is_panel_on(self):
        return _read('panel')

    def set_panel(self, onoff):
        _write('panel', onoff)


class ControlSimulation(object):
    def __init__(self, keys):
        self.keys = keys
        self.solenoid_state = None
        self.panel_state = None

    def set_ready_led(self, onoff):
        print('control: led_ready', onoff)

    def set_play_led(self, onoff):
        print('control: led_play', onoff)

    def set_solenoid(self, onoff):
        self.solenoid_state = onoff
        print('control: solenoid', onoff)

    def is_solenoid_on(self):
        return self.solenoid_state

    async def eject_solenoid(self):
        print('control: eject_solenoid')
        if self.is_solenoid_on():
            self.set_solenoid(False)
            while self.keys.any_keys_pressed():
                await asyncio.sleep(0.25)
            self.set_solenoid(True)

    def is_panel_on(self):
        return self.panel_state

    def set_panel(self, onoff):
        self.panel_state = onoff
        print("control: panel", onoff)
