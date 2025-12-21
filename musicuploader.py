import services
import json
import datetime
import argparse
import subprocess
import glob
from pathlib import Path
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

# TODO
# Figure out what the flow is
# 
# Make album or single
# Read in metadata
# Process .wav and .png coverart into relevant exports (video, .mp3, .webp, etc)
# Soure files - .wav and .png
# - mp3 (add tags & cover art)
# - mp4 (create video w/coverart & music)
# - webp (ludoloon website)
# Move files to any relevant places
# Upload to youtube
# Prep data for manual upload to: itch, newgrounds and patreon (make it easy to copy and paste)
# Publicize launch: ludoloon.studio, bluesky, mastodon, instagram and (hopefully) discord

# Pre-processing
def read_json(fname="release.json"):
    release_info = []
    with open(fname) as f:
        release_info = json.load(f)
        #release_info["date"] = datetime.datetime.strptime(release_info["date"], "%Y-%m-%d")

    return release_info

def preprocessing(args, release_info):
    '''The process of creating .mp3, .mp4, .webp, etc'''
    cover_path=Path(args.content_dir, args.cover)

    for wav_file in glob.glob(args.content_dir + "/*.wav"):
        create_mp3(wav_file, release_info)
        create_mp4(wav_file, cover=cover_path)
    #Create .webp version of cover art for ludoloon.studio
    create_webp(cover_path)

def create_mp3(source_file, json, dest_path=None):
    '''Use the shell to run LAME and create an MP3, add tags'''
    #Create file
    if dest_path is None:
        dest_path = str(source_file)[:-3] + "mp3"
    subprocess.run(["lame", "-V0", source_file, dest_path])

    #Add MP3 tags
    mp3 = MP3(dest_path, ID3=EasyID3)
    mp3.add_tags()  #Add EasyID3 header
    mp3["title"] = json["title"]
    mp3["date"] = json["date"]
    tags = ["artist", "website", "genre", "album"]
    for tag in tags:
        mp3[tag] = json["mp3"][tag]
    mp3.save()

def create_mp4(source_file, dest_path=None, cover="Cover.png"):
    '''Use the shell to run lame and create an MP4'''
    
    if dest_path is None:
        dest_path = source_file[:-3] + "mp4"
    
    subprocess.run(["ffmpeg", "-loop", "1", "-i", cover, "-i", source_file, "-shortest",
                    "-c:v", "libx264", "-tune", "stillimage", "-c:a", "copy", dest_path])

def create_webp(cover, dest_path=None):
    if dest_path is None:
        dest_path = str(cover)[:-3] + "webp"

    subprocess.run(["magick", cover, "-quality", "90", dest_path])

if __name__ == "__main__":
    #Construct the parser
    parser = argparse.ArgumentParser(
        prog='Music Uploader',
        description="Utility to quickly upload music releases online",
        epilog="(Author: Pierce - LudoLoon Studio, ludoloon.studio)")
    
    #Add arguments
    parser.add_argument("content_dir", help="Root directory of music content")
    parser.add_argument("--json", type=str, default="release.json", 
                        help="Specify a release.json config file")
    parser.add_argument("--cover", type=str, default="Cover.png", 
                        help="Specify the name of the cover art image")

    #Parse arguments
    args = parser.parse_args() 

    # Read metadata and store into release info
    release_info = read_json(args.json)
    preprocessing(args, release_info)