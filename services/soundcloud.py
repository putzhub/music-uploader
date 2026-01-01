# API docs - https://developers.soundcloud.com/docs/api/guide#uploading
#Just copy & paste for now

import webbrowser
import services

DEFAULT_TAGS = ["royalty-free", "indie", "bgm", "vgm"]

def upload(release):
    '''Prep copy & paste material for Soundcloud, grab url when done.'''
    #Just do the first one and assume that's fine until we actually spec this for albums
    print(services.prep_post(release, services.Service.SOUNDCLOUD))

    webbrowser.open("https://soundcloud.com/upload")
    url = input("What is the project URL on Soundcloud?")
    return url