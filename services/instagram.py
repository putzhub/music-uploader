import webbrowser
import services

DEFAULT_TAGS = ["music", "asset", "gameaudio", "vgm", "bgm", "royaltyfreemusic", 
          "soundtrack", "indie", "renoise", "composer", "game", "videogame",
          "gamemusic", "ost", "pack", "bundle"]

def post(release, testing=False):
    '''Create an easy message to copy and paste for instagram.'''
    print(services.prep_post(release, services.Service.BSKY))
    webbrowser.open("https://instagram.com")
    input("Welp, did ya post it to instagram? [press enter]")
    return True