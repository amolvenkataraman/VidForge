import requests
from gtts import gTTS

from lib.utils import gen_randstr


def make_gtts_audio(text: str, lang='en', tld='ca'):
    tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
    fn = f"Temp/AUDIO_{gen_randstr(6)}.mp3"
    tts.save(fn)

    return fn

def make_brian_audio(text: str):
    r = requests.get(f"https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={text}")
    fn = f"Temp/AUDIO_{gen_randstr(6)}.mp3"
    with open(fn, "wb") as f:
        f.write(r.content)
    
    return fn

