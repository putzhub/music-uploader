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

if __name__ == "__main__":
    # Read metadata and store into release info
    release_info = []
    with open("release.json") as f:
        release_info = json.load(f)
        release_info["date"] = datetime.datetime.strptime(release_info["date"], "%Y-%m-%d")

    #Construct the parser
    parser = argparse.ArgumentParser(
        prog='Music Uploader',
        description="Utility to quickly upload music releases online",
        epilog="(Not sure what this does)")
    
    #Add arguments
    #parser.add_argument("--help")

    #Parse arguments
    parser.parse_args()