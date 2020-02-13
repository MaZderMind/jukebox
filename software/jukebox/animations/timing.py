import asyncio
import itertools
from collections.abc import Iterable

from animations.animation_solid import solid
from animations.animation_utils import FPS
from animations.color_utils import from_hex
from animations.dip_utils import dip_direct
from animations.sender import Sender


class TimingController(object):
    def __init__(self, sender=None):
        self.sender = sender or Sender()

    async def run_for(self, stop_after_seconds, animation_generator):
        num_frames = stop_after_seconds * FPS
        for n, frame in enumerate(animation_generator):
            self.sender.display_frame(frame)
            await asyncio.sleep(1 / FPS)

            if n > num_frames:
                break

    async def run_forever(self, animation_generator):
        for frame in animation_generator:
            self.sender.display_frame(frame)
            await asyncio.sleep(1 / FPS)


class Sequencer(object):
    def __init__(self, sender, animation_producer_or_list_of_animations):
        self.sender = sender or Sender()

        if isinstance(animation_producer_or_list_of_animations, Iterable):
            self.animation_producer = None
            self.animation_iterable = itertools.cycle(animation_producer_or_list_of_animations)
        else:
            self.animation_producer = animation_producer_or_list_of_animations
            self.animation_iterable = None

        self.seconds_per_animation = 60 * 3
        self.fade_function = dip_direct
        self.seconds_for_fade = 1
        self._interrupted = False
        self.stopped = True

    def interrupt(self):
        print("interrupting...")
        self._interrupted = True

    def stop(self):
        print("stopping animation loop...")
        self.sender.blackout()
        self.stopped = True

    def _next_animation(self):
        if self.animation_iterable is not None:
            return next(self.animation_iterable)
        else:
            return self.animation_producer()

    async def run(self):
        current_animation = solid(from_hex('00000'))
        self.stopped = False

        while True:
            print("start dip")
            last_animation = current_animation
            next_animation = self._next_animation()

            num_frames = int(self.seconds_for_fade * FPS)
            print("num_frames", num_frames)
            for n in range(num_frames):
                last_frame = next(last_animation)
                next_frame = next(next_animation)
                frame = self.fade_function(last_frame, next_frame, n / num_frames)
                self.sender.display_frame(frame)
                await asyncio.sleep(1 / FPS)

            current_animation = next_animation
            print("dip done")

            num_frames = int(self.seconds_per_animation * FPS)
            print("num_frames", num_frames)
            for n, frame in enumerate(current_animation):
                self.sender.display_frame(frame)
                await asyncio.sleep(1 / FPS)

                if self._interrupted:
                    print("interrupted")
                    self._interrupted = False
                    break

                if self.stopped:
                    print("stopped")
                    return

                if n > num_frames:
                    break
