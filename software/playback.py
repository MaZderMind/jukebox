from spotify import Spotify


class Playback(object):
    def __init__(self, conf):
        self.spotify = Spotify(conf)
        self.spotify.login()
        self.conf = conf['playback']
        self.playing_prefix = None

    def can_start(self, key_combo):
        if key_combo not in self.conf:
            print("unconfigured key-combo", key_combo)
            return False

        target = self.conf[key_combo]
        prefix, target = target.split(':', 1)
        if prefix not in Playback.HANDLERS:
            print("unknown prefix", prefix)
            return False

        return True

    def start(self, key_combo):
        target = self.conf[key_combo]
        prefix, target = target.split(':', 1)
        Playback.HANDLERS[prefix](self, target)

        self.playing_prefix = prefix

    def pause(self):
        if self.playing_prefix is None:
            return

        Playback.HANDLERS[self.playing_prefix](self, None)
        self.playing_prefix = None

    def is_playing(self):
        return self.playing_prefix is not None

    def _handle_spotify(self, target):
        if target is not None:
            print("starting spotify with target", target)
            self.spotify.play("spotify:" + target)
        else:
            print("pausing spotify")
            self.spotify.pause()

    HANDLERS = {
        "spotify": _handle_spotify,
    }
