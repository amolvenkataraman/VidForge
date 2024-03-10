import os
import glob
import math
import random

from moviepy.editor import *
from moviepy.video.fx.all import *


def crop_video(clip, ar: list):
    cs = clip.size

    if cs[0] / cs[1] == ar[0] / ar[1]: return clip

    if ar[0] / ar[1] >= cs[0] / cs[1]:
        cw = cs[0]
        ch = cs[0] * ar[1] / ar[0]
    else:
        ch = cs[1]
        cw = cs[1] * ar[0] / ar[1]

    clip = crop(
        clip,
        x_center=clip.size[0] // 2,
        y_center=clip.size[1] // 2,
        width=cw,
        height=ch,
    )

    return clip

def make_background_clip(length: float, path: str):
    fp = random.choice(glob.glob(f"{os.getcwd()}/{path}"))

    clip = VideoFileClip(fp)
    loc = random.randint(1, math.floor(clip.duration) - math.ceil(length) - 1)
    clip = clip.subclip(loc, loc + length)

    return clip
