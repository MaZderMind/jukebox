from ffplay import FFplay
from playback_handler import PlaybackHandler


class Radio(PlaybackHandler, FFplay):
    def pause(self):
        self.stop_ffplay()

    def is_playing(self):
        return self.is_ffplay_running()

    def play(self, target):
        print("starting radio", target)
        self.start_ffplay(target)
