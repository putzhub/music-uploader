import services
import json
import argparse
import subprocess
import zipfile
import os
import logging
from datetime import date

from glob import glob
from copy import deepcopy
from pathlib import Path
from mutagen.id3 import ID3
from mutagen.id3._frames import APIC
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from PIL import Image

__VERSION__ = "2026.9.23.0"

#Start the logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# TODO
# Deal with encoding track info into filename:
#   i.e: BPM (look at fmod or whatever format)
# Add album exporting
# - Skip unwanted services or specify which ones
# - Refactor code to make more sense for a multi-song approach
#TODO: Specify which services to skip or use
#TODO Add more services:
# - Bandcamp(text), Fab/Unreal(text), Lemmy(API), Archive.org(API), Unity (Cmdline?), Jamendo(text), Gamedevmarket(text)

REQUIRED_KEYS = {
    "root": ["file", "title", "summary", "date", "url", "tags"],
    "details": ["bpm", "cost", "loop", "genre"],
    "mp3": ["album", "artist", "website"]
}

class MusicRelease():
    #Class variables
    tracks = []
    content_dir = ""
    source_dir = ""
    output_dir = ""
    cover_file = ""
    json_file = ""

    def __init__(self, json_file, content_dir, output_dir="", cover_file="Cover.png"):
        #Content dir is the root of all our work
        self.content_dir = content_dir
        self.tracks = []

        #Read JSON file, relative to content_dir if it's just a filename, otherwise relative to CWD.
        self.json_file = Path(content_dir, json_file) if str(Path(json_file).parent) == "." else Path(json_file)
        if self.json_file.exists():
            self.load()
        else:
            self.create()
            
        #Source path is where files we build with live, assign as output dir if none is provided
        source = Path(content_dir, "Source")
        self.source_dir = source if source.exists() else self.content_dir
        if not Path(output_dir).exists() and output_dir != "":
            os.makedirs(output_dir)
        self.output_dir = output_dir if output_dir != "" else self.source_dir

        #Check if cover file actually exists
        self.cover_file = str(Path(self.source_dir, cover_file)) if Path(self.source_dir, cover_file).exists() else ""
        
        #Make sure we have the expected keys in the json file (and hopefully by extension data)
        for entry in self.tracks:
            for group in  REQUIRED_KEYS:
                for key in REQUIRED_KEYS[group]:
                    if group != "root":
                        assert key in entry[group]
                    else:
                        assert key in entry
    
    #Helpers
    def load(self):
        '''Load a release.json file and read its contents'''
        logger.debug(f"Loading file: {self.json_file}")
        with open(self.json_file) as f:
            self.tracks = json.load(f)

    def save(self):
        '''Save tracks[] JSON metadata to the file being read from.'''
        logger.debug(f"Saving file: {self.json_file}")
        with open(self.json_file, "w") as f:
            f.write(json.dumps(self.tracks, indent=4))

    def create(self):
        '''Create a new release.json'''
        logger.info("Creating a new .json for release!")

        template = {}
        for group in REQUIRED_KEYS:
            if group != "root":
                template[group] = {}
            for key in REQUIRED_KEYS[group]:
                if group != "root":
                    template[group][key] = ""
                else:
                    template[key] = ""

        file_names = glob(f"{self.content_dir}/*.wav")
        guess = len(file_names)
        logging.info("Hitting enter below will automatically detect file paths for .json, otherwise it's manual.")
        try:
            num_tracks = input(f"How many tracks are there [if {guess} hit enter]: ")
            num_tracks = guess if num_tracks == "" else int(num_tracks)                    
        except ValueError:
            logger.warning("Invalid input, assuming 1 track")
            num_tracks = 1

        template["mp3"]["artist"] = input("What is the artist name? [Enter to leave blank] ")
        template["mp3"]["album"] = input("What is the album name? [Enter to leave blank] ")
        template["mp3"]["website"] = input("What is the website? [Enter to leave blank] ")
        album_date = input("What date was the release? [Enter for today] ")
        template["date"] = album_date if album_date != "" else str(date.today())

        png_files = glob(f"{self.content_dir}/*.png")
        if len(png_files) == 1:
            template["cover"] = png_files[0]
        else:
            png_file = input(f"Set Cover path [hit enter if {self.cover_file}]: ")
            template["cover"] = png_file if png_file != "" else self.cover_file
        
        for i in range(num_tracks):
            self.tracks.append(deepcopy(template))
            if num_tracks == guess:
                # We can assume every .wav is a track with an entry
                self.tracks[-1]["file"] = file_names[i]
                self.tracks[-1]["title"] = file_names[i][2:-4]
        
        self.save()
        logger.info("New release.json created! Program will exit so you can fill out the details in the new file.")
        exit()

    #Preprocess the source material into the needed files
    def preprocessing(self, overwrite=False):
        '''The process of creating .mp3, .mp4, .webp, etc'''
        logger.debug(f"Start preprocssing. Overwrite: {overwrite}")

        #Iterate over each track in the pack
        for (i, track) in enumerate(self.tracks):
            #Build the filename paths
            wav_file = Path(self.source_dir, track["file"])
            mp3_path = Path(self.output_dir, wav_file.stem + ".mp3")
            mp4_path = Path(self.output_dir, wav_file.stem + ".mp4")
            webp_file = Path(self.output_dir, self.tracks[i]["cover"])

            #Create files
            if (mp3_path.exists() and overwrite) or not mp3_path.exists():
                create_mp3(wav_file, self.tracks[i], mp3_path, self.cover_file)

            if self.cover_file != "":
                if (mp4_path.exists() and overwrite) or not mp4_path.exists():
                    create_mp4(wav_file, mp4_path, self.cover_file)
                #Create .webp version of cover art for ludoloon.studio
                if self.tracks[i]["cover"]:
                    if (webp_file.exists() and overwrite) or not webp_file.exists():
                        create_webp(self.cover_file, webp_file)
            else:
                logger.warning("Cover file not found, skipping .mp4 & .webp in preprocessing", )

        #If we have stems or patterns then assume we should pack this into a .zip
        zip_file = Path(self.output_dir, "Release.zip")

        if Path(self.source_dir, "Stems/").exists() or Path(self.source_dir, "Patterns/"):
            logger.debug("Stems or Patterns folder found.")
            if (zip_file.exists() and overwrite) or not zip_file.exists():
                create_zip(self.source_dir, zip_file)
        
        logger.debug("Preprocessing complete.")

    #Upload music online
    def upload_music(self):
        #WARNING: NOT THOROUGHLY TESTED FOR MULTIPLE FILES - First file assumed as default metadata after youtube
        logger.debug("Uploading music...")
        #Upload tracks to remaining hosting services
        platforms = {
            "youtube": "streaming",
            "itch": "stores", 
            "newgrounds": "streaming",
            "soundcloud": "streaming"
        }
        for platform in platforms:
            #Iterate through places to upload to accounting for whether store or streaming
            logger.debug(f"Checking for existing link: {platform}")

            #"streaming" or "stores"
            style = platforms[platform]
            for track in self.tracks:
                #If streaming or stores aren't in the .json yet, add them
                track["streaming"] = {} if "streaming" not in track else track["streaming"]
                track["stores"] = {} if "stores" not in track else track["stores"]

                #If we don't have a link yet, add one.
                if platform not in track[style]:
                    logger.debug(f"Existing link not found, uploading to {platform}")
                    #use the platform name to let us call the upload method
                    urls = getattr(services, platform).upload(self)
                    #Apply the link to *all* tracks
                    if platform == "youtube":
                        for i, track in enumerate(self.tracks):
                            #Skip if a track wasn't uploaded (should already exist)
                            if urls[i] == ('', ''):
                                continue
                            #First entry in tuple is embed url, Second youtu.be/
                            track["embed"] = urls[i][0]
                            track[style][platform] = urls[i][1]
                    else:
                        #Figure out if we have multiple urls or not and apply to all tracks
                        for track in self.tracks:
                            if type(urls) == str:
                                track[style][platform] = urls
                            else:
                                track[style][platform] = str(urls[0])
                        
                    #save after creating the URL for relevant page
                    self.save()
    
    def promote(self):
        #Put automated ones last in case we fuck up on the non-automated ones.
        social_media = ["bsky", "instagram", "patreon", "lls", "mastoposter"]

        for platform in social_media:
            getattr(services, platform).post(self)

#Preprocessing helpers
def create_mp3(source_file, json, dest_path=None, cover=""):
    '''Use the shell to run LAME and create an MP3, add tags'''
    #Create file
    if dest_path is None:
        dest_path = str(source_file)[:-3] + "mp3"
    
    logger.debug(f"Creating mp3 of {source_file} at {dest_path}")
    subprocess.run(["lame", "--quiet", "-V0", "-h", source_file, dest_path])

    #Add MP3 tags
    mp3 = MP3(dest_path, ID3=EasyID3)
    logger.debug("Adding mp3 tags...")
    mp3.add_tags()  #Add EasyID3 header

    #Write tags to their relevant spots
    for tag in ["title", "date"]:
        mp3[tag] = json[tag]
    for tag in ["artist", "website", "album"]:
        mp3[tag] = json["mp3"][tag]
    mp3["genre"] = json["details"]["genre"]
    mp3.save()

    #Add cover if available
    if cover != "":
        logger.debug(f"Adding cover image to mp3 file {dest_path}")
        with open(cover, 'rb') as art:
            audio = ID3(dest_path)
            audio.add(
                    APIC(
                        encoding=3, # 3 is for utf-8
                        mime='image/png', # image/jpeg or image/png
                        type=3, # 3 is for the cover image
                        desc=u'Cover',
                        data=art.read()
                    )
                )
            audio.save()
    
def create_mp4(source_file, dest_path=None, cover="Cover.png"):
    '''Use the shell to run ffmpeg and create an MP4'''
    if dest_path is None:
        dest_path = str(source_file)[:-3] + "mp4"

    logger.debug(f"Creating mp4 of {source_file} using {cover} at {dest_path}")
    #Make an mp4 exactly the length of the song and add black borders to make it 16:9 for youtube
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-loop", "1", "-i", cover, "-i", source_file, "-shortest",
                    "-c:v", "libx264", "-tune", "stillimage", "-c:a", "copy", "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1", dest_path])

def create_webp(src_path, dest_path=None):
    '''Use the shell to run ImageMagick to convert to .webp'''
    if dest_path is None:
        dest_path = str(src_path)[:-3] + "webp"
    
    logger.debug(f"Creating mp3 of {src_path} at {dest_path}")

    with Image.open(src_path) as img:
        # PNGs support transparency, which WebP also supports.
        # However, if the image has a palette (e.g., PNG-8), converting to 'RGB' 
        # or 'RGBA' first is often safer for saving to other formats.
        if img.mode in ('P', 'LA', 'L'):
            img = img.convert('RGBA')
        img.save(dest_path, "WEBP", quality=85)

def create_zip(source, dest_path=None):
    '''Create an archive of source at dest_path'''
    if dest_path is None:
        dest_path = str(source + ".zip")

    logger.debug(f"Creating zip of {source} at {dest_path}")

    with zipfile.ZipFile(dest_path, "w", compression=zipfile.ZIP_DEFLATED) as zip:
        #Recurse the directory, only zip WAV files though
        for path in Path(source).rglob("*.wav"):
            #Remove source path from archive file names
            trunc = len(str(source))
            zip.write(path, str(path)[trunc:])

if __name__ == "__main__":
    #Construct the parser
    parser = argparse.ArgumentParser(
        prog='Music Uploader',
        description="Utility to quickly upload music releases online",
        epilog="(Author: Pierce - LudoLoon Studio, ludoloon.studio)")
    
    #Add arguments
    parser.add_argument("content_dir", 
                        help="Root directory of music content")
    parser.add_argument("--promote", action="store_true",
                        help="Publish to social media channels")
    parser.add_argument("--json", type=str, default="release.json", 
                        help="Specify a release.json config file (default: ./release.json)")
    parser.add_argument("--cover", type=str, default="Cover.png", 
                        help="Specify the filename of the PNG cover art image (FILENAME ONLY, default: Cover.png)")
    parser.add_argument("--output", type=str, default="",
                        help="Specify an output directory other than the source directory")
    parser.add_argument("--overwrite", action="store_true", default=False,
                        help="Preprocessing should overwrite the .mp3, .mp4, .webp, .zip files")
    parser.add_argument("--upload", action="store_true", default=False,
                        help="Preprocessing should overwrite the .mp3, .mp4, .webp, .zip files")
    parser.add_argument("--verbose", action="store_true", default=False,
                        help="Display advanced logging info.")
    parser.add_argument("--version", action="version", version=f"Music-Uploader Version: {__VERSION__}")

    #Parse arguments
    args = parser.parse_args() 

    #Set logging
    log_level = logging.INFO if not args.verbose else logging.DEBUG
    logger.setLevel(log_level)
    
    # Read metadata and store into release info
    music_release = MusicRelease(args.json, 
                                args.content_dir, 
                                args.output, 
                                cover_file=args.cover)
    music_release.preprocessing(args.overwrite)
    if args.upload is True:
        music_release.upload_music()
    if args.promote is True:
        music_release.promote()
