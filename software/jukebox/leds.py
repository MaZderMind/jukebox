import asyncio
from enum import Enum, auto

from animations.animation_meter import meter
from animations.animation_solid import solid
from animations.sender import Sender
from animations.timing import Sequencer

SHOW_STRIP0_IMMEDIATE = b'\x11'

CMD_BLACKOUT = b'\x00'


class State(Enum):
    BLACKOUT = auto()
    IDLE = auto()
    ACTIVE = auto()


class Leds(object):
    def __init__(self, conf):
        self.seq = Sequencer(
            Sender(conf['host'], conf['port']),
            self._animation_selector
        )
        self.state = State.BLACKOUT

    def _animation_selector(self):
        if self.state == State.BLACKOUT:
            return solid((0, 0, 0))
        elif self.state == State.IDLE:
            return solid((.5, .5, .5))
        elif self.state == State.ACTIVE:
            return meter()

    def blackout(self):
        self.state = State.BLACKOUT
        self.seq.stop()

    def _start_or_interrupt(self):
        if self.seq.stopped:
            asyncio.create_task(self.seq.run())
        else:
            self.seq.interrupt()

    def idle(self):
        self.state = State.IDLE
        self._start_or_interrupt()

    def show(self, key_combo):
        self.state = State.ACTIVE
        self._start_or_interrupt()


class LedsSimulation(object):

    def blackout(self):
        print("leds: blackout")

    def idle(self):
        print("leds: idle")

    def show(self, key_combo):
        print("leds: show", key_combo)
