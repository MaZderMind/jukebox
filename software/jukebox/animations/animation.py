import abc


class Animation(abc.ABC):
    @abc.abstractmethod
    def matrix_generator(self, rows, leds_per_row):
        pass

    def strip_generator(self, leds):
        yield from self.matrix_generator(1, leds)
