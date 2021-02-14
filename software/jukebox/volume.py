import alsaaudio
import evdev

DEFAULT_VOLUME = 90


def clamp(value, smallest, largest):
    return max(smallest, min(value, largest))


class Volume(object):
    def __init__(self, conf):
        self.conf = conf['volume']
        self.volume_device = None
        self.alsa_mixer = None

    def reset_volume(self):
        print(f"Resetting Volume back to {DEFAULT_VOLUME}%")
        self.alsa_mixer.setvolume(DEFAULT_VOLUME)

    async def open_device(self):
        volume_device = [
            evdev.InputDevice(dev) for dev in evdev.list_devices() if
            evdev.InputDevice(dev).name == self.conf['input_device_name']
        ]

        if len(volume_device) == 0:
            self.print_missing_device_error()
            raise VolumeError()

        self.volume_device = volume_device[0]
        self.alsa_mixer = alsaaudio.Mixer(self.conf['alsa_mixer_name'])

    def print_missing_device_error(self):
        panel_names = [
            evdev.InputDevice(dev).name for dev in evdev.list_devices()
        ]
        print("no input-device with name", self.conf['input_device_name'],
              "found. The following devices are registered", panel_names)

    async def handle_events(self):
        async for event in self.volume_device.async_read_loop():
            if event.code == evdev.ecodes.REL_MISC and event.type == evdev.ecodes.EV_REL:
                self.adjust_volume(event.value)

    def adjust_volume(self, amount):
        current_volume = self.alsa_mixer.getvolume()[0]
        new_volume = clamp(current_volume + amount, 0, 100)
        self.alsa_mixer.setvolume(new_volume)


class VolumeError(RuntimeError):
    pass
