import subprocess

current_proc = None


class FFplay(object):
    def stop_ffplay(self):
        global current_proc
        if current_proc is not None:
            print("terminating ffmepg")
            current_proc.terminate()
            current_proc = None

    def is_ffplay_running(self):
        global current_proc
        if current_proc is not None:
            poll = current_proc.poll()
            return poll is None

        return False

    def start_ffplay(self, url, stdin=subprocess.DEVNULL):
        global current_proc
        self.stop_ffplay()
        print("starting ffmepg", url)
        current_proc = subprocess.Popen(["ffplay", "-autoexit", "-nodisp", url],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL,
                                        stdin=stdin)
