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
Classification: Soundtrack

Description:
-----
<em>{0}</em>

<h4>Technical Details</h4>
<ul>
<li><strong>License: Creative Commons International 4.0 Attribution (Royalty Free)</strong></li>
<li><strong>Number of tracks:</strong> {4}</li>
<li><strong>Format:</strong> .wav (44.1khz / 16-bit) & .mp3 (VBR) / {2} / Stereo</li>
<li><strong>Style:</strong> {3} </li>
<li><strong>BPM:</strong></li>
</ul>

<h4>Contact</h4>
<a href="mailto:support@ludoloon.studio">Support & inquiries</a> | <a href="mailto:connect@ludoloon.studio">Send your promo</a>
<a href="https://www.patreon.com/c/ludoloonstudio/">Patreon (Stems & More!)</a> | <a href="https://ludoloon.studio/hire">Available for hire</a>

<h4>More Music</h4>
<ul>
<li><a href="https://ludoloon.studio">LudoLoon Studio Homepage</a></li>
<li><a href="https://www.patreon.com/c/ludoloonstudio/home">Patreon (stems & early tracks!)</a></li>
<li><a href="https://youtube.com/channel/UCziXXRaD4uUuTL7tMWtQeVQ">Youtube</a></li>
<li><a href="https://https://ludoloonstudio.itch.io/">More on Itch.io!</a></li>
</ul>

-----
Tags: royalty-free, music, asset-pack, indie, wav, {3}
'''.format(args["title"], 
           args["summary"], 
           args["details"]["loop"], 
           ", ".join(args["tags"]), 
           len(json),
           args["details"]["bpm"]))

    webbrowser.open("https://itch.io/game/new")
    itch_url = input("What is the project URL on itch.io?")
    return itch_url