from copy import deepcopy
import webbrowser

def upload(json):
    '''Prep copy & paste material for itch.io, grab url when done.'''

    #Just do the first one and assume that's fine until we actually spec this for albums
    args = deepcopy(json[0])

    print(
'''
Title: {0}
Tagline: {1}
License: Creative commons, allow sharealike

Classification: Soundtrack
-----
Description:
-----

{1}

Format: .MP3 (VBR)
Style: {2}
BPM: {4}

--More Music--
homepage: https://ludoloon.studio/music
itch.io: {3}
patreon (get stems & tracks in advance): https://patreon.com/ludoloonstudio

-----
Tags: royalty-free, indie, bgm, vgm, {2}
'''.format(args["title"], 
           args["summary"], 
           ", ".join(args["tags"]), 
           args["stores"]["itch"],
           args["details"]["bpm"],
           args["embed"]))

    webbrowser.open("https://www.newgrounds.com/projects/audio/new")
    url = input("What is the project URL on Newgrounds?")
    return url