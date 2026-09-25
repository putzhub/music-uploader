# Read Me

# About

This is a personal project to make my life easier when uploading music to the web.

It probably won't be as useful to the broader public, but who knows!

Regardless, you'll need a few things to be true:

1. You're on linux (windows, mac, etc not tested)
2. You have the following installed:
   * LAME, ffmpeg, ImageMagick, (tbd)

## Setup

0. Setup venv:

`python -m venvsource .venv/bin/activate`

1. Install dependencies: python3 -m pip install -r requirements.txt
2. Setup Google api access: https://cloud.google.com (make sure youtube data api is enabled for uploading).
3. Create a folder called "secrets" for your login details in the root folder of this app (readme.md and secrets/ should be visible in your file browswer)
4. For youtube, put OAuth2 api ID & secret into "client_secrets.json" (rename from client_secrets_example.json)
5. For Mastodon on the Developers section ([mastodon.instance]/settings/applications) make a file called "mastodoncred.secrets" an application with access to post with your account and put Client Key, Client Secret and Your Access Token, with a line return after each entry (in that order).
6. For Bluesky put your login and password (make an app password under Privacy & Security) in "bluesky.secrets"

## Usage

Run musicuploader.py in the directory where your music is, or pass in a path that can find where your source content is (.wavs, .pngs, etc). You will be asked some questions to initialize the file. Fill out the release.json that gets made and run the application again once finished.

Required in source content dir:

* at least a .wav file.
* You can include a .png, .jpg or .webp cover, which will be included as the mp3 album art, made into an mp4 and if desired, converted to .webp.

Output will be written to the source folder unless an ouput dir is specified.

If you'd like to seperate source material from other files you can structure the folder as so:

* CONTENT_DIRECTORY/
  * Source/
    * Stems/
      * [...]
    * Cover.png
    * files.wav
    * [...]
  * Other Folders/
  * Other files...

Alternatively the folder passed via commandline will default as the source directory, or current working directory if none.

If any folder is found with .wav files (such as stems) a zip will be created with all .wav files.