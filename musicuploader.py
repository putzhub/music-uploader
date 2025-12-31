import services
import json
import argparse
import subprocess
import zipfile
import os
import shutil

from pathlib import Path
from mutagen.id3 import APIC, ID3
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from PIL import Image


# TODO
# Add album exporting
#Figure out where release.json should live
#TODO: Specify which services to skip or use
#TODO Add more services: Bandcamp, Soundcloud, Jamendo, Archive.org, Godot marketplace, Unity, Unreal, Gamedevmarket
#Implement logger

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
        if not Path(self.output_dir).exists():
            os.makedirs(self.output_dir)
        #Cover path - deal with custom, default or no cover at all.
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
            create_mp3(wav_file, self.tracks[i], mp3_path, self.cover_file)
            if self.cover_file != "":
                mp4_path = Path(self.output_dir, wav_file.stem + ".mp4")
                create_mp4(wav_file, mp4_path, self.cover_file)
                #Create .webp version of cover art for ludoloon.studio
                if self.tracks[i]["cover"]:
                    webp_file = Path(self.output_dir, self.tracks[i]["cover"])
                    if not webp_file.exists():
                        create_webp(self.cover_file, webp_file)
            else:
                print("Cover file not found, skipping .mp4 & .webp in preprocessing", )

        #If we have stems or patterns then package them
        if Path(self.source_dir, "Stems/").exists() or Path(self.source_dir, "Patterns/"):
            zip_name = self.tracks[0]["album"] if "album" in self.tracks[0] else self.tracks[0]["title"]
            create_zip(self.source_dir, Path(self.output_dir, str(zip_name + ".zip")))

    #Upload music online
    def upload_music(self):
        #WARNING: NOT TESTED FOR MULTIPLE FILES - First file assumed as default metadata after youtube
        
        #Upload tracks to remaining hosting services
        platforms = {
            "youtube": "streaming",
            "itch": "stores", 
            "newgrounds": "streaming"
        }
        for platform in platforms:
            #Iterate through places to upload to accounting for whether store or streaming
            try:
                #"streaming" or "stores"
                style = platforms[platform]
                #if this fails we need to create it
                self.tracks[0][style][platform]
            except KeyError:
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
        social_media = ["mastoposter", "bksy", "instagram", "patreon", "lls"]

        for platform in social_media:
            getattr(services, platform).post(self)

#Preprocessing helpers
def create_mp3(source_file, json, dest_path=None, cover=""):
    '''Use the shell to run LAME and create an MP3, add tags'''
    #Create file
    if dest_path is None:
        dest_path = str(source_file)[:-3] + "mp3"
    subprocess.run(["lame", "--quiet", "-V0", "-h", source_file, dest_path])

    #Add MP3 tags
    mp3 = MP3(dest_path, ID3=EasyID3)
    mp3.add_tags()  #Add EasyID3 header
    #Write tags to their relevant spots
    for tag in ["title", "date"]:
        mp3[tag] = json[tag]
    for tag in ["artist", "website", "genre", "album"]:
        mp3[tag] = json["mp3"][tag]
    mp3.save()
    #Add cover if available
    if cover != "":
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
    #Make an mp4 exactly the length of the song and add black borders to make it 16:9 for youtube
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-loop", "1", "-i", cover, "-i", source_file, "-shortest",
                    "-c:v", "libx264", "-tune", "stillimage", "-c:a", "copy", "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1", dest_path])

def create_webp(src_path, dest_path=None):
    '''Use the shell to run ImageMagick to convert to .webp'''
    if dest_path is None:
        dest_path = str(src_path)[:-3] + "webp"
    
    with Image.open(src_path) as img:
        # PNGs support transparency, which WebP also supports.
        # However, if the image has a palette (e.g., PNG-8), converting to 'RGB' 
        # or 'RGBA' first is often safer for saving to other formats.
        if img.mode in ('P', 'LA', 'L'):
            img = img.convert('RGBA')
        img.save(dest_path, "WEBP", quality=85)

def create_zip(source, dest_path=None):
    '''Create an archive'''
    if dest_path is None:
        dest_path = str(source + ".zip")

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
                        help="Specify a release.json config file")
    parser.add_argument("--cover", type=str, default="Cover.png", 
                        help="Specify the filename of the PNG cover art image (FILENAME ONLY, default: Cover.png)")
    parser.add_argument("--output", type=str, default="",
                        help="Specify an output directory other than the source directory")

    #Parse arguments
    args = parser.parse_args() 

    # Read metadata and store into release info
    music_release = MusicRelease(args.json, args.content_dir, args.output, cover_file=args.cover)
    music_release.preprocessing()
    music_release.upload_music()
    if args.promote is True:
        #print(args.promote)
        music_release.promote()
