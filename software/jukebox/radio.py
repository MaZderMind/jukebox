import subprocess

from playback_handler import PlaybackHandler


class Radio(PlaybackHandler):
    def __init__(self):
        self._proc = None

    def pause(self):
        if self._proc is not None:
            print("stopping radio")
            self._proc.terminate()
            self._proc = None

    def is_playing(self):
        if self._proc is not None:
            poll = self._proc.poll()
            return poll is None

        return False

    def play(self, target):
        print("starting radio", target)
        self._proc = subprocess.Popen(["ffplay", "-autoexit", "-nodisp", target],
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL)
