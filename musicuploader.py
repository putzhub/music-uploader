import services
import json
import datetime
import argparse

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

def read_json(fname="release.json"):
    release_info = []
    with open(fname) as f:
        release_info = json.load(f)
        release_info["date"] = datetime.datetime.strptime(release_info["date"], "%Y-%m-%d")

    return release_info

if __name__ == "__main__":
    # Read metadata and store into release info
    release_info = read_json()
   

    #Construct the parser
    parser = argparse.ArgumentParser(
        prog='Music Uploader',
        description="Utility to quickly upload music releases online",
        epilog="(Author: Pierce - LudoLoon Studio, ludoloon.studio)")
    
    #Add arguments
    parser.add_argument("--json", type="", help="Specify a release.json file")

    #Parse arguments
    parser.parse_args()

    #Continue through workflow...