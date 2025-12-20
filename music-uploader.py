import services.youtube
import json

# TODO
# Figure out what the flow is
# 
# Read in metadata
# Process .wav and .png coverart into relevant exports (video, .mp3, .webp, etc)
# Move files to any relevant places
# Upload to youtube
# Prep data for manual upload to: itch, newgrounds and patreon (make it easy to copy and paste)
# Publicize launch: ludoloon.studio, bluesky, mastodon, instagram and (hopefully) discord

if __name__ == "__main__":
    release_info = ""
    with open("release.json") as f:
        release_info = json.load(f)

    print(release_info)