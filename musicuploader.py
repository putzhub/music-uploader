import services
import json
import argparse
import subprocess
import glob
import shutil

from pathlib import Path
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


# TODO
# Figure out what the flow is
# Scenarios:
#   1. Single release
#   2. Album release (same album)
#   3. Multiple individual releases (probably not though)
# 
# Make single (ALBUM EXPORTING NOT YET SUPPORTED)
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

class MusicRelease():
    #Class Variables
    tracks = []
    content_dir = ""
    source_dir = ""
    output_dir = ""
    cover_file = ""
    json_file = ""

    def __init__(self, json_file, content_dir, output_dir="", cover_file="Cover.png"):
        #Init variables
        self.json_file = json_file
        #Content dir is the root of all our work
        self.content_dir = content_dir
        #Source path is where files we build with live
        source = Path(content_dir, "Source")
        self.source_dir = source if source.exists() else self.content_dir
        self.output_dir = output_dir if output_dir != "" else self.source_dir
        #Cover path
        self.cover_file = Path(self.source_dir, cover_file) if Path(self.source_dir, cover_file).exists() else ""
        #read in from JSON file
        self.load()
        
        #Make sure we have the expected keys (and hopefully by extension data)
        for entry in self.tracks:
            for key in ["title", "summary", "date", "url", "tags"]:
                assert key in entry
            #Do the same for MP3 and Details tags
            for key in ["bpm", "cost", "loop", "stems"]:
                assert key in entry["details"]
            for key in ["genre", "album", "artist", "website"]:
                assert key in entry["mp3"]
    
    #Helpers
    def load(self):
        with open(self.json_file) as f:
            self.tracks = json.load(f)

    def save(self):
        '''Save our tracks[] JSON metadata to the file we read from.'''
        with open(self.json_file,"w") as f:
            f.write(json.dumps(self.tracks, indent=4))

    #Preprocess the source material into the needed files
    def preprocessing(self):
        '''The process of creating .mp3, .mp4, .webp, etc'''

        #Iterate over each track in the pack
        for (i, track) in enumerate(self.tracks):
            #Build the filename
            wav_file = Path(self.source_dir, track["title"] + ".wav")

            #Create files
            mp3_path = Path(self.output_dir, wav_file.stem + ".mp3")
            mp4_path = Path(self.output_dir, wav_file.stem + ".mp4")
            create_mp3(wav_file, self.tracks[i], mp3_path)
            create_mp4(wav_file, mp4_path, self.cover_file)
            #Create .webp version of cover art for ludoloon.studio
            if self.tracks[i]["cover"]:
                webp_file = Path(self.output_dir, self.tracks[i]["cover"])
                if not webp_file.exists():
                    create_webp(self.cover_file, webp_file)

        #If we have stems then package them
        stems_path = Path(self.source_dir, "Stems/")
        if stems_path.exists():
            create_zip(stems_path, Path(self.output_dir, "Stems"))

    #Upload music online
    def upload_music(self):
        #WARNING: NOT TESTED FOR MULTIPLE FILES - First file assumed as default metadata after youtube
        #TODO: Specify which services to skip or use

        #Youtube first
        for (i, track) in enumerate(self.tracks):
            #Converting to string avoids issues, but deepcopy() on services.youtube.upload may make this irrelevant.
            mp4 = str(Path(self.output_dir, track["title"] + ".mp4"))
            ytid = services.youtube.upload(mp4, track)
            if ytid is not False:
                self.tracks[i]["embed"] = str("https://youtube.com/embed/"+ytid)
                self.save()
        
        #TODO Add soundcloud to the mix

        #Itch.io & Newgrounds- assume that all music will be on same page, use first track to check if online yet or not
        platforms = {"itch": "stores", "newgrounds": "streaming"}
        for platform in platforms:
            #Iterate through places to upload to accounting for whether store or streaming
            try:
                #"streaming" or "stores"
                style = platforms[platform]
                self.tracks[0][style][platform]
            except KeyError:
                #use the platform name to let us call the upload method
                url = getattr(services, platform).upload(self.tracks)
                #Apply the link to *all* tracks
                for track in self.tracks:
                    track[style][platform] = str(url)
                #save after creating the URL for relevant page
                self.save()

#Preprocessing helpers
def create_mp3(source_file, json, dest_path=None):
    '''Use the shell to run LAME and create an MP3, add tags'''
    #Create file
    if dest_path is None:
        dest_path = str(source_file)[:-3] + "mp3"
    subprocess.run(["lame", "--quiet", "-V0", "-h", source_file, dest_path])

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
    '''Use the shell to run ffmpeg and create an MP4'''
    if dest_path is None:
        dest_path = str(source_file)[:-3] + "mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-loop", "1", "-i", cover, "-i", source_file, "-shortest",
                    "-c:v", "libx264", "-tune", "stillimage", "-c:a", "copy", dest_path])

def create_webp(cover, dest_path=None):
    '''Use the shell to run ImageMagick to convert to .webp'''
    if dest_path is None:
        dest_path = str(cover)[:-3] + "webp"
    subprocess.run(["magick", cover, "-quality", "90", dest_path])

def create_zip(source, dest_path=None):
    "Create an archive"
    if dest_path is None:
        dest_path = str(source)
    shutil.make_archive(dest_path, "zip", source)

if __name__ == "__main__":
    #Construct the parser
    parser = argparse.ArgumentParser(
        prog='Music Uploader',
        description="Utility to quickly upload music releases online",
        epilog="(Author: Pierce - LudoLoon Studio, ludoloon.studio)")
    
    #Add arguments
    parser.add_argument("content_dir", 
                        help="Root directory of music content")
    parser.add_argument("--json", type=str, default="release.json", 
                        help="Specify a release.json config file")
    parser.add_argument("--cover", type=str, default="Cover.png", 
                        help="Specify the name of the cover art image")
    parser.add_argument("--promote", action="store_true",
                        help="Publish to social media channels")

    #Parse arguments
    args = parser.parse_args() 

    # Read metadata and store into release info
    music_release = MusicRelease(args.json, args.content_dir)
    music_release.preprocessing()
    music_release.upload_music()
    if args.promote is True:
        print(args.promote)
        #music_release.promote()
