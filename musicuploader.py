import services
import json
import datetime
import argparse
import subprocess

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

def preprocessing(content_dir, release_info):
    '''The process of creating .mp3, .mp4, .webp, etc'''
    #Create MP3
    #Create MP4
    #Create webp
    pass

def create_mp3(source_file, dest_file):
    '''Use the shell to run lame and create an MP3'''
    if dest_file is None:
        subprocess.run(["lame", "-V0", source_file])
    else:
        subprocess.run(["lame", "-V0", source_file, dest_file])

if __name__ == "__main__":
    #Construct the parser
    parser = argparse.ArgumentParser(
        prog='Music Uploader',
        description="Utility to quickly upload music releases online",
        epilog="(Author: Pierce - LudoLoon Studio, ludoloon.studio)")
    
    #Add arguments
    parser.add_argument("content_dir", help="Root directory of music content")
    parser.add_argument("--json", type=str, help="Specify a release.json config file")

    #Parse arguments
    args = parser.parse_args() 

    # Read metadata and store into release info
    release_info = read_json(args.json)
    preprocessing(args.content_dir, release_info)