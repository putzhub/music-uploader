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
Youtube-Embed: {6}
Classification: Soundtrack

Description:
-----
<em>{1}</em>

<h4>Technical Details</h4>
<ul>
<li><strong>License: Creative Commons International 4.0 Attribution (Royalty Free)</strong></li>
<li><strong>Number of tracks:</strong> {4}</li>
<li><strong>Format:</strong> .WAV <em>(44.1khz / 16-bit)</em> | .MP3 <em>(VBR)</em> / {2} / Stereo</li>
<li><strong>Style:</strong> {3} </li>
<li><strong>BPM:</strong> {5}</li>
</ul>

<h4>Contact</h4>
<a href="mailto:support@ludoloon.studio">Support & inquiries</a> | <a href="mailto:connect@ludoloon.studio">Send your promo with my music</a>
<a href="https://www.patreon.com/c/ludoloonstudio/">Patreon (Stems & More!)</a> | <a href="https://ludoloon.studio/hire">Available for hire</a>

<h4>More Music</h4>
<ul>
<li><a href="https://ludoloon.studio">Homepage - LudoLoon Studio</a></li>
<li><a href="https://ludoloonstudio.bandcamp.com/">Bandcamp</a></li>
<li><a href="https://ludoloonstudio.newgrounds.com/audio">Newgrounds</a></li>
<li><a href="https://soundcloud.com/ludoloonstudio">Soundcloud</a></li>
<li><a href="https://youtube.com/channel/UCziXXRaD4uUuTL7tMWtQeVQ">Youtube</a></li>
<li><a href="https://ludoloonstudio.itch.io/">More on Itch.io!</a></li>
</ul>

<h4>Socials</h4>
<a href="https://bsky.app/profile/ludoloonstudio.bsky.social">Bluesky</a> | <a href="https://instagram.com/ludoloonstudio/">Instagram</a> | <a href="https://mastodon.gamedev.place/@ludoloon">Mastodon</a>

-----
Tags: royalty-free, music, asset-pack, indie, wav, {3}

BG: #222
BG2: #333
Text: #eaeaea
Link: #2ce8f4
'''.format(args["title"], 
           args["summary"], 
           args["details"]["loop"], 
           ", ".join(args["tags"]), 
           len(json),
           args["details"]["bpm"],
           args["embed"]))

    webbrowser.open("https://itch.io/game/new")
    itch_url = input("What is the project URL on itch.io?")
    return itch_url