import random

import cv2
import praw
import pytesseract
from PIL import Image
import numpy as np
from moviepy.editor import *

from lib.background import *
from lib.image import *
from lib.tts import *
from lib.utils import *


def gen_title(title, size):
    title_audio = AudioFileClip(make_brian_audio(title["text"]))
    title_splash = (
        TextClip(
            title["text"],
            fontsize=title["size"],
            stroke_width=4,
            font=title["font"],
            color='white',
            stroke_color='black',
            method='caption',
            size=(size[0] * 0.8, size[1] * 0.3)
    ).set_position('center').set_duration(title_audio.duration + title["wait_time"])).set_audio(title_audio)

    return title_splash

def gen_text(text, size, location, duration):
    text = (
        TextClip(
            text["text"],
            fontsize=text["size"],
            font=text["font"],
            stroke_width=2,
            color='white',
            stroke_color='black',
            method='caption',
            size=(size[0], size[1] * 0.2)
    ).set_position(location).set_duration(duration))

    return text

def memes_simple(memes, background, output_file, render, **kwargs):
    # Keep a running tally of total video duration and a list of clips
    total_len = 0
    clips = []

    # Iterate through memes
    for m in memes:
        # Make TTS background audio
        aud = AudioFileClip(make_brian_audio(m[1]))
        # Download image and make a clip of it
        img = ImageClip(get_image_from_path(m[0])) \
            .set_duration(aud.duration + 0.5) \
            .set_pos(("center","center")) \
            .resize(width=background["size"][0] * 0.9) \
            .set_audio(aud)
        # Update length and clips list
        total_len += img.duration
        clips.append(img)

    if "front_title" in kwargs.keys():
        # Add a splash title to the front if one is required
        front_title_splash = gen_title(kwargs["front_title"], background["size"])

        clips.insert(0, front_title_splash)
        total_len += front_title_splash.duration

    if "back_title" in kwargs.keys():
        # Add a splash title to the back if one is required
        back_title_splash = gen_title(kwargs["back_title"], background["size"])

        clips.append(back_title_splash)
        total_len += back_title_splash.duration

    # Concatenate all the foreground clips
    video = concatenate(clips, method="compose")
    # Generate a background clip
    clip = crop_video(make_background_clip(total_len, background["location"]), background["aspect_ratio"]).resize(tuple(background["size"]))

    # Compose the foreground and background to make a result and save it
    result = CompositeVideoClip([clip, video.set_position('center')])

    if "top_text" in kwargs.keys():
        top_text = gen_text(kwargs["top_text"], background["size"], "top", result.duration)
        result = CompositeVideoClip([result, top_text])

    if "bottom_text" in kwargs.keys():
        bottom_text = gen_text(kwargs["bottom_text"], background["size"], "bottom", result.duration)
        result = CompositeVideoClip([result, bottom_text])

    result.write_videofile(output_file, fps=render["fps"], codec=render["codec"], bitrate=render["bitrate"], threads=render["threads"])

    # Clean up any temporary files
    clean_up("temp/*")

def memes_simple_file(memes_file, background, output_file, render, **kwargs):
    # Open the file that has links to memes and captions
    with open(memes_file, "r") as f:
        memes = [m.rstrip().split("  ", 1) for m in f.read().split("\n")]

    # Call the meme video generator
    memes_simple(
        memes=memes,
        background=background,
        output_file=output_file,
        render=render,
        **kwargs
    )

def memes_simple_multiple(memes_file, vid_size, background, output_file, render, **kwargs):
    # Open memes file, read lines and randomize the order
    with open(memes_file, "r") as f:
        lines = f.read().split("\n")
        random.shuffle(lines)

    # Generate the content of all the individual files
    files = [lines[i:i + vid_size] for i in range(0, len(lines), vid_size)]

    # Iterate through the files
    for i, f in enumerate(files):
        # Save the file in the temporary folder
        fn = f"temp/MEME_{gen_randstr(6)}.txt"
        with open(fn, "w") as ff:
            ff.write("\n".join(f))

        # Call the meme video generator
        memes_simple_file(
            title=title,
            memes_file=fn,
            background=background,
            output_file=output_file.replace("%", i),
            render=render,
            **kwargs
        )

def preprocess_finale(im):
    im= cv2.bilateralFilter(im,5, 55,60)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    _, im = cv2.threshold(im, 240, 255, 1)
    return im

def memes_simple_reddit(reddit, subreddit, vid_size, background, output_file, render, **kwargs):
    reddit = praw.Reddit(**reddit)
    memes = []
    for m in list([i.url for i in reddit.subreddit(subreddit).hot(limit=vid_size)]):
        try:
            ml = get_image_from_path(m)
            mc = pytesseract.image_to_string(preprocess_finale(np.array(Image.open(ml))))
            if mc.rstrip() != "":
                memes.append([ml, mc])
        except: continue
    
    # Call the meme video generator
    memes_simple(
        memes=memes,
        background=background,
        output_file=output_file,
        render=render,
        **kwargs
    )
