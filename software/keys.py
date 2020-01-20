import evdev


class Keys(object):
    def __init__(self, conf):
        self.conf = conf
        self.panel_device = None

    async def open_device(self):
        panel_name = self.conf['input_device_name']

        panel_device = [
            evdev.InputDevice(dev) for dev in evdev.list_devices() if
            evdev.InputDevice(dev).name == panel_name
        ]

        if len(panel_device) == 0:
            self.print_missing_device_error()
            raise KeysError()

        panel_device = panel_device[0]
        panel_device.repeat = [0, 0]

        self.panel_device = panel_device

    def print_missing_device_error(self):
        panel_names = [
            evdev.InputDevice(dev).name for dev in evdev.list_devices()
        ]
        print("no input-device with name", self.conf['input_device_name'],
              "found. The folloging devides are registered", panel_names)

    async def wait_for_event(self):
        last_active_keys = None

        async for event in self.panel_device.async_read_loop():
            active_keys = self.panel_device.active_keys()

            if active_keys != last_active_keys:
                yield Keys.keys_to_key_combo(active_keys)
                last_active_keys = active_keys

    @classmethod
    def keys_to_key_combo(cls, active_keys):
        # FIXME 1 handling
        alpha_keycodes = [evdev.ecodes.KEY_A, evdev.ecodes.KEY_B, evdev.ecodes.KEY_C, evdev.ecodes.KEY_D,
                          evdev.ecodes.KEY_E, evdev.ecodes.KEY_F, evdev.ecodes.KEY_G, evdev.ecodes.KEY_H, None,
                          evdev.ecodes.KEY_J, evdev.ecodes.KEY_K, evdev.ecodes.KEY_L, evdev.ecodes.KEY_M,
                          evdev.ecodes.KEY_N, evdev.ecodes.KEY_O, evdev.ecodes.KEY_P, evdev.ecodes.KEY_Q]

        numeric_keycodes = [None, evdev.ecodes.KEY_2, evdev.ecodes.KEY_3, evdev.ecodes.KEY_4,
                            evdev.ecodes.KEY_5, evdev.ecodes.KEY_6, evdev.ecodes.KEY_7, evdev.ecodes.KEY_8]

        alpha_key = None
        number_key = None
        for key in active_keys:
            if key in alpha_keycodes:
                index = alpha_keycodes.index(key)
                alpha_key = str(chr(ord('A') + index))

            if key in numeric_keycodes:
                index = numeric_keycodes.index(key)
                number_key = str(chr(ord('1') + index))

        if alpha_key is not None and number_key is not None:
            return alpha_key + number_key

        return None


class KeysError(RuntimeError):
    pass
