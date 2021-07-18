import asyncio
import itertools
from collections.abc import Iterable
from typing import Optional

from animations.animation import Animation
from animations.animation_solid import Solid
from animations.animation_utils import FPS
from animations.color_utils import from_hex, linear_interpolate_frame
from animations.sender import Sender


class TimingController(object):
    def __init__(self, conf):
        self.conf = conf

    async def run_forever(self, animation: Animation):
        matrix_sender = Sender(self.conf['host'], self.conf['port'])
        matrix_generator = animation.matrix_generator(self.conf['rows'], self.conf['leds_per_row'])

        strips = [
            (
                Sender(strip['host'], strip['port'], strip.get('index', 0)),
                animation.strip_generator(strip['leds'])
            )
            for strip in self.conf['strips']
        ]

        while True:
            matrix_sender.display_frame(next(matrix_generator))
            for sender, generator in strips:
                sender.display_frame(next(generator))

            await asyncio.sleep(1 / FPS)


class FrameSet(object):
    def __init__(self, matrix_frame, strip_frames):
        self.matrix_frame = matrix_frame
        self.strip_frames = strip_frames


class SenderManager(object):
    def __init__(self, conf):
        self.matrix_sender = Sender(conf['host'], conf['port'])
        self.strip_senders = [
            Sender(strip['host'], strip['port'], strip.get('index', 0))
            for strip in conf['strips']
        ]

    def blackout(self):
        self.matrix_sender.blackout()
        for strip_sender in self.strip_senders:
            strip_sender.blackout()

    def display_frame_set(self, frameset: FrameSet):
        self.matrix_sender.display_frame(frameset.matrix_frame)
        for i, strip_sender in enumerate(self.strip_senders):
            strip_frame = frameset.strip_frames[i]
            strip_sender.display_frame(strip_frame)


class AnimationManager(object):
    def __init__(self, conf, animation):
        self.matrix_animation = animation.matrix_generator(conf['rows'], conf['leds_per_row'])
        self.strip_animations = [
            animation.strip_generator(strip['leds'])
            for strip in conf['strips']
        ]

    def get_frame_set(self) -> FrameSet:
        return FrameSet(
            matrix_frame=next(self.matrix_animation),
            strip_frames=[
                next(strip_animation)
                for strip_animation in self.strip_animations
            ]
        )


class AnimationStateManager(object):
    def __init__(self, conf, initial_animation: Animation):
        self.conf = conf
        self.current_animation: AnimationManager = AnimationManager(self.conf, initial_animation)
        self.next_animation: Optional[AnimationManager] = None

    def stage_next_animation(self, next_animation):
        self.next_animation = AnimationManager(self.conf, next_animation)

    def proceed_to_next_animation(self):
        self.current_animation = self.next_animation
        self.next_animation = None

    def get_frame_set_from_current_animation(self) -> FrameSet:
        return self.current_animation.get_frame_set()

    def get_frame_set_next_current_animation(self) -> FrameSet:
        return self.next_animation.get_frame_set()

    def get_faded_frame_set(self, frac) -> FrameSet:
        current_frame_set = self.get_frame_set_from_current_animation()
        next_frame_set = self.get_frame_set_next_current_animation()
        return FrameSet(
            matrix_frame=linear_interpolate_frame(
                current_frame_set.matrix_frame,
                next_frame_set.matrix_frame,
                frac
            ),
            strip_frames=[
                linear_interpolate_frame(
                    current_frame_set.strip_frames[i],
                    next_frame_set.strip_frames[i],
                    frac
                )
                for i in range(len(current_frame_set.strip_frames))
            ]
        )


class Sequencer(object):
    def __init__(self, conf, animation_producer_or_list_of_animations):
        self.conf = conf
        self.senders = SenderManager(self.conf)
        self.animations = AnimationStateManager(conf, Solid(from_hex('000000')))

        if isinstance(animation_producer_or_list_of_animations, Iterable):
            self.animation_producer = None
            self.animation_iterable = itertools.cycle(animation_producer_or_list_of_animations)
        else:
            self.animation_producer = animation_producer_or_list_of_animations
            self.animation_iterable = None

        self.seconds_per_animation = 60 * 3
        self.seconds_for_fade = 1
        self._interrupted = False
        self.stopped = True

    def interrupt(self):
        print("interrupting...")
        self._interrupted = True

    def stop(self):
        print("stopping animation loop...")
        self.senders.blackout()
        self.stopped = True

    def choose_next_animation(self):
        if self.animation_iterable is not None:
            return next(self.animation_iterable)
        else:
            return self.animation_producer()

    async def run(self):
        self.stopped = False

        while True:
            next_animation = self.choose_next_animation()
            print("chose next_animation=%s, start dip" % next_animation)
            self.animations.stage_next_animation(next_animation)

            num_frames = int(self.seconds_for_fade * FPS)
            print("num_frames", num_frames)
            for n in range(num_frames):
                frame_set = self.animations.get_faded_frame_set(n / num_frames)
                self.senders.display_frame_set(frame_set)
                await asyncio.sleep(1 / FPS)

            self.animations.proceed_to_next_animation()
            print("dip done")

            num_frames = int(self.seconds_per_animation * FPS)
            print("num_frames", num_frames)
            for n in range(0, num_frames):
                frame_set = self.animations.get_frame_set_from_current_animation()
                self.senders.display_frame_set(frame_set)
                await asyncio.sleep(1 / FPS)

                if self._interrupted:
                    print("interrupted")
                    self._interrupted = False
                    break

                if self.stopped:
                    print("stopped")
                    return
