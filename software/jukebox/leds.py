import asyncio
from enum import Enum, auto

import named_animations
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
    def __init__(self, conf, animations):
        self.seq = Sequencer(
            Sender(conf['host'], conf['port']),
            self._animation_selector
        )
        self.state = State.BLACKOUT
        self.animations = animations
        self._animation_name = None

    def _animation_selector(self):
        if self.state == State.BLACKOUT:
            return solid((0, 0, 0))
        elif self.state == State.IDLE:
            return solid((.5, .5, .5))
        elif self.state == State.ACTIVE:
            if self._animation_name is None:
                return solid((0, 0, 0))

            if isinstance(self._animation_name, list):
                method = self._animation_name[0]
                attr = self._animation_name[1:]
                return getattr(named_animations, method)(*attr)
            else:
                return getattr(named_animations, self._animation_name)()

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
        letter = key_combo[0]
        if key_combo in self.animations:
            self._animation_name = self.animations[key_combo]
        elif letter in self.animations:
            self._animation_name = self.animations[letter]
        else:
            self._animation_name = None

        print("starting animation", self._animation_name)
        self._start_or_interrupt()


class LedsSimulation(object):

    def blackout(self):
        print("leds: blackout")

    def idle(self):
        print("leds: idle")

    def show(self, key_combo):
        print("leds: show", key_combo)
