# Read Me

# About

This is a personal project to make my life easier when uploading music to the web.

It probably won't be as useful to the broader public, but who knows!

Regardless, you'll need a few things to be true:

1. You're on linux
2. You have the following installed:
    * LAME, ffmpeg, ImageMagick, (tbd)

## Setup
0. Setup venv: 

``` python -m venv ``` 
``` source .venv/bin/activate ```

1. Install dependencies: python3 -m pip install -r requirements.txt
2. Setup Google api access: https://cloud.google.com (make sure youtube data api is enabled for uploading).
3. Create a folder called "secrets" for your login details in the root folder of this app (readme.md and secrets/ should be visible in your file browswer)
3. For youtube, put OAuth2 api ID & secret into "client_secrets.json" (rename from client_secrets_example.json)
4. For Mastodon on the Developers section ([mastodon.instance]/settings/applications) make a file called "mastodoncred.secrets" an application with access to post with your account and put Client Key, Client Secret and Your Access Token, with a line return after each entry (in that order).
5. For Bluesky put your login and password (make an app password under Privacy & Security) in "bluesky.secrets"

## Usage

To use music-uploader.py, fill out a release.json file with the relevant information (see release_example.json).

It expects at minimum a .wav file. Titles in the release.json file must match filenames of the .wavs you want processed. You can include a .png Cover, which will be included as the mp3 album art, made into an mp4 and converted to .webp.

Output will be written to the source folder unless an ouput dir is specified.

If you'd like to seperate source material from other files you can structure the folder as so:

CONTENT_DIRECTORY/
    - Source/
        Stems/
            [...]
        Cover.png
        files.wav
        [...]
    - Other Folders/
    - Other files...

Alternatively the folder passed via commandline will default as the source directory.

If a Stems or Patterns folder is found a zip will be created with any .wav files in the source dir.