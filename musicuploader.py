import services
import json
import datetime
import argparse
import subprocess
import glob
from pathlib import Path

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
        release_info["date"] = datetime.datetime.strptime(release_info["date"], "%Y-%m-%d")

    return release_info

def preprocessing(args, release_info):
    '''The process of creating .mp3, .mp4, .webp, etc'''
    for wav_file in glob.glob(args.content_dir + "/*.wav"):
        cover=Path(args.content_dir, args.cover)
        #Create MP3
        create_mp3(wav_file)
        #Create MP4
        create_mp4(wav_file, cover=cover)
    #Create webp
    #create_webp(cover)

def create_mp3(source_file, dest_file=None):
    '''Use the shell to run lame and create an MP3'''
    if dest_file is None:
        subprocess.run(["lame", "-V0", source_file])
    else:
        subprocess.run(["lame", "-V0", source_file, dest_file])

def create_mp4(source_file, dest_file=None, cover="Cover.png"):
    '''Use the shell to run lame and create an MP4'''
    
    if dest_file is None:
        dest_file = source_file[:-3] + "mp4"
    
    subprocess.run(["ffmpeg", "-loop", "1", "-i", cover, "-i", source_file, "-shortest",
                    "-c:v", "libx264", "-tune", "stillimage", "-c:a", "copy", dest_file])

def create_webp():
    pass

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