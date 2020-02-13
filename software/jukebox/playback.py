from radio import Radio
from spotify import Spotify


class Playback(object):
    def __init__(self, conf):
        spotify = Spotify(conf)
        spotify.login()

        radio = Radio()

        self.handlers = {
            "spotify": spotify,
            "radio": radio
        }

        self.conf = conf['playback']
        self.playing_prefix = None

    def can_start(self, key_combo):
        if key_combo not in self.conf:
            print("unconfigured key-combo", key_combo)
            return False

        target = self.conf[key_combo]
        prefix, target = target.split(':', 1)
        if prefix not in self.handlers:
            print("unknown prefix", prefix)
            return False

        return True

    def start(self, key_combo):
        target = self.conf[key_combo]
        prefix, target = target.split(':', 1)
        self.playing_prefix = prefix
        self._get_handler().play(target)

    def pause(self):
        if self.playing_prefix is None:
            return False

        self._get_handler().pause()
        self.playing_prefix = None

    def is_playing(self):
        if self.playing_prefix is None:
            return False

        return self._get_handler().is_playing()

    def _get_handler(self):
        return self.handlers[self.playing_prefix]
