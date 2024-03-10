import os
import glob
import random
import string


def gen_randstr(length: int) -> str:
    return ''.join(
        random.choice(string.ascii_lowercase)
        for i in range(length)
    )

def clean_up(path: str):
    for f in glob.glob(path):
        os.remove(f)
