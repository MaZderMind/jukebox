import asyncio
import itertools

from animation_utils import FPS
from color_utils import rgb_gamma, to_byte
from dip_utils import dip_direct
from send import send


def send_as_bytes(frame):
    pixels = [to_byte(rgb_gamma(pixel)) for pixel in frame]
    msg = bytes(itertools.chain.from_iterable(pixels))
    send(msg)


async def run_for(stop_after_seconds, animation_generator):
    num_frames = stop_after_seconds / FPS
    for n, frame in enumerate(animation_generator):
        send_as_bytes(frame)
        await asyncio.sleep(1 / FPS)

        if n > num_frames:
            break


async def run_forever(animation_generator):
    for frame in animation_generator:
        send_as_bytes(frame)
        await asyncio.sleep(1 / FPS)


async def run_animation_sequence(animation_generators,
                                 seconds_per_animation=60 * 3,
                                 fade_function=dip_direct,
                                 seconds_for_fade=1,
                                 state_probe=lambda: None):
    current_animation = next(animation_generators)
    last_state = state_probe()

    while True:
        try:
            num_frames = int(seconds_per_animation * FPS)
            print("num_frames", num_frames)
            for n, frame in enumerate(current_animation):
                send_as_bytes(frame)
                await asyncio.sleep(1 / FPS)

                new_state = state_probe()
                if last_state != state_probe():
                    last_state = new_state
                    break

                if n > num_frames:
                    break

            print("start dip")
            last_animation = current_animation
            next_animation = next(animation_generators)

            num_frames = int(seconds_for_fade * FPS)
            print("num_frames", num_frames)
            for n in range(num_frames):
                last_frame = next(last_animation)
                next_frame = next(next_animation)
                frame = fade_function(last_frame, next_frame, n / num_frames)
                send_as_bytes(frame)
                await asyncio.sleep(1 / FPS)

            current_animation = next_animation
            print("dip done")
        except StopIteration:
            break
