#LudoLoon Studio
from pathlib import Path
from os import getcwd
import subprocess
import shutil

#hard code this since it's my own website anyway
WEBSITE_DIR = Path("/home/pootz/Documentos/Websites/LudoLoonStudio/ludoloon.studio")
IMAGE_DIR = Path(WEBSITE_DIR, "content/images/covers/")
MUSIC_DATA = Path(WEBSITE_DIR, "content/music_data.js")

def post(release):
    src = Path(release.output_dir, release.tracks[0]["cover"])
    dest = Path(IMAGE_DIR)
    print(src)
    shutil.copy(src, dest)

    subprocess.call(["kate", MUSIC_DATA, release.json_file])
    input("Have you copied the release JSON into the music database? [PRESS ENTER]")