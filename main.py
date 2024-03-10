import os
import sys
sys.path.append(os.getcwd())
import json
import time
import argparse

from scripts.memes import memes_simple

RUNNABLE_SCRIPTS = ["memes_simple"]

def run_command(conf):
    if conf["command"] in RUNNABLE_SCRIPTS:
        globals()[conf["command"]](**conf)
    else:
        raise Exception("Invalid command")

parser = argparse.ArgumentParser(
    prog="VidForge",
    description="Automatically generate different types of videos"
)
parser.add_argument('-c', '--config', help="Path to JSON configuration file", required=True)


if __name__ == '__main__':
    args = parser.parse_args()

    start = time.time()

    if os.path.isfile(args.config):
        conf = json.load(open(args.config, "r"))
        run_command(conf)
    else:
        raise Exception("Configuration file not found")

    print(f"DONE! {time.time() - start:.2f} seconds.")
