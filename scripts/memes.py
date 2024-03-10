from moviepy.editor import *

from lib.background import *
from lib.image import *
from lib.tts import *
from lib.utils import *

def memes_simple(name, memes_file, background, output, threads: int=8, **kwargs):
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
    
    total_len = title_audio.duration
    clips = [title_splash]

    with open(memes_file, "r") as f:
        for m in f.read().split("\n"):
            ml, mc = m.rstrip().split("  ", 1)
            aud = AudioFileClip(make_brian_audio(mc))
            img = ImageClip(get_image_from_url(ml)) \
                .set_duration(aud.duration + 1) \
                .set_pos(("center","center")) \
                .resize(width=background["size"][0] * 0.9) \
                .set_audio(aud)
            total_len += img.duration
            clips.append(img)
    
    video = concatenate(clips, method="compose")
    clip = crop_video(make_background_clip(total_len + 1, background["location"]), background["aspect_ratio"]).resize(tuple(background["size"]))

    result = CompositeVideoClip([clip, video.set_position('center')])
    result.write_videofile(output["file"], fps=output["fps"], codec=output["codec"], bitrate=output["bitrate"], threads=threads)

    clean_up("Temp/*")
