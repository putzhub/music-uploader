import webbrowser
import services

DEFAULT_TAGS = ["royalty-free", "indie", "bgm", "vgm"]

def upload(release):
    '''Prep copy & paste material for itch.io, grab url when done.'''
    #Overwrite "release" so that our previous code assumption of a single track works
    release = release.tracks[0]

    #Just do the first one and assume that's fine until we actually spec this for albums
    print(services.prep_post(release, services.Service.NEWGROUNDS))

    webbrowser.open("https://www.newgrounds.com/projects/audio/new")
    url = input("What is the project URL on Newgrounds?")
    return url