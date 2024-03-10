from moviepy.editor import *

from lib.background import *
from lib.image import *
from lib.tts import *
from lib.utils import *


def memes_simple(name, memes_file, background, output, threads: int=8, **kwargs):
    # Make title splash and background TTS (ex. "DANK MEMES")
    title_audio = AudioFileClip(make_brian_audio(name))
    title_splash = (
        TextClip(
            name,
            fontsize=100,
            font='Cantarell-Bold',
            color='white',
            method='caption',
            size=(background["size"][0] * 0.8, background["size"][1] * 0.3)
    ).set_position('center').set_duration(title_audio.duration + 1)).set_audio(title_audio)
    
    # Keep a running tally of total video duration and a list of clips
    total_len = title_audio.duration
    clips = [title_splash]

    # Open the file that has links to memes and captions
    with open(memes_file, "r") as f:
        for m in f.read().split("\n"): # Iterate through lines
            ml, mc = m.rstrip().split("  ", 1)
            # Make TTS background audio
            aud = AudioFileClip(make_brian_audio(mc))
            # Download image and make a clip of it
            img = ImageClip(get_image_from_url(ml)) \
                .set_duration(aud.duration + 1) \
                .set_pos(("center","center")) \
                .resize(width=background["size"][0] * 0.9) \
                .set_audio(aud)
            # Update length and clips list
            total_len += img.duration
            clips.append(img)
    
    # Concatenate all the foreground clips
    video = concatenate(clips, method="compose")
    # Generate a background clip
    clip = crop_video(make_background_clip(total_len + 1, background["location"]), background["aspect_ratio"]).resize(tuple(background["size"]))

    # Compose the foreground and background to make a result and save it
    result = CompositeVideoClip([clip, video.set_position('center')])
    result.write_videofile(output["file"], fps=output["fps"], codec=output["codec"], bitrate=output["bitrate"], threads=threads)

    # Clean up any temporary files
    clean_up("temp/*")
