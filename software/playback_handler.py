import abc


class PlaybackHandler(abc.ABC):
    @abc.abstractmethod
    def play(self, target):
        pass

    @abc.abstractmethod
    def pause(self):
        pass

    @abc.abstractmethod
    def is_playing(self):
        pass