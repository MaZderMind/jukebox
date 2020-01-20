from spotify import Spotify


class Playback(object):
    def __init__(self, conf):
        self.spotify = Spotify(conf)

    def start(self, key_combo):
        pass

    def pause(self):
        pass