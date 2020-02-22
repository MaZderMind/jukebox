import subprocess

from ffplay import FFplay
from playback_handler import PlaybackHandler

global current_proc


class YoutubeDl(PlaybackHandler, FFplay):
    def pause(self):
        self.stop_ffplay()

    def is_playing(self):
        return self.is_ffplay_running()

    def play(self, url):
        global current_proc
        self.stop_ffplay()
        print("starting youtube_dl", url)
        current_proc = subprocess.Popen(["youtube-dl", "-o", "-", url],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.DEVNULL)

        return self.start_ffplay("-", stdin=current_proc.stdout)
