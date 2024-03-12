import os
import requests

from lib.utils import gen_randstr


def get_image_from_path(path: str):
    if "http://" in path or "https://" in path:
        r = requests.get(path)
        fn = f"temp/IMG_{gen_randstr(6)}.jpg"
        with open(fn, "wb") as f:
            f.write(r.content)
        return fn
    else:
        return path
