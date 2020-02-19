import subprocess


class FFplay(object):
    def __init__(self):
        self._proc = None

    def stop_ffplay(self):
        if self._proc is not None:
            print("terminating ffmepg")
            self._proc.terminate()
            self._proc = None

    def is_ffplay_running(self):
        if self._proc is not None:
            poll = self._proc.poll()
            return poll is None

        return False

    def start_ffplay(self, url):
        self.stop_ffplay()
        print("starting ffmepg", url)
        self._proc = subprocess.Popen(["ffplay", "-autoexit", "-nodisp", url],
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL)
