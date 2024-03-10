import os
import requests

from lib.utils import gen_randstr


def get_image_from_url(url: str):
    r = requests.get(url)
    fn = f"temp/IMG_{gen_randstr(6)}.jpg"
    with open(fn, "wb") as f:
        f.write(r.content)
    
    return fn