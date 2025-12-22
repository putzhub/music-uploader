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
3. Put OAuth2 api ID & secret into client_secrets.json (rename from client_secrets_example.json)
4. (in progress)

## Usage

To use music-uploader.py, fill out a release.json file with the relevant information (see release_example.json).

Structure a folder as so:

CONTENT_DIRECTORY/
    - Source/
        Stems/
            [...]
        Cover.png
        files.wav
        [...]

Titles in the release.json file must match filenames of the .wavs you want processed.