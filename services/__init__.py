from enum import Enum
from copy import deepcopy

from . import bsky
from . import discord
from . import instagram
from . import itch
from . import lls
from . import mastoposter
from . import patreon
from . import reddit
from . import soundcloud
from . import youtube
from . import newgrounds
from . import archiveorg

class Service(Enum):
    BSKY = bsky
    DISCORD = discord
    INSTAGRAM = instagram
    ITCH = itch
    LLS = lls
    MASTODON = mastoposter
    PATREON = patreon
    REDDIT = reddit
    SOUNDCLOUD = soundcloud
    YOUTUBE = youtube
    NEWGROUNDS = newgrounds
    ARCHIVEORG = archiveorg

def combine_tags(*args, separator=" ", prepend=""):
    '''Combine an open ended number of arrays into a single combination of tags as a string.'''
    combined_array = []

    for arg in args:
        for list in arg:
             combined_array.append(list)

    #give 'em hashtags and remove inner tag spaces
    combined_array = [str(prepend+tag).replace(" ", "") for tag in combined_array]
    combined_array = separator.join(combined_array)

    return combined_array

#TODO Piece out message builder functions for common info groups maybe?
def prep_post(release, service):
    msg = ""
    module = service.value
    #First track data only, for where it's relevant
    try:
        track = release.tracks[0]
    except AttributeError:
        track = release

    #MASTODON & BLUESKY
    if service == Service.MASTODON or service == Service.BSKY:
        msg = f'''
{track["summary"]}

{track["streaming"]["youtube"]}

{combine_tags(module.DEFAULT_TAGS, track["tags"], prepend="#")}
'''
    
    #INSTAGRAM
    elif service == Service.INSTAGRAM:
        msg = f'''
{track["summary"]}

See link in bio for more.

{combine_tags(module.DEFAULT_TAGS, track["tags"], prepend="#")}
'''
    
    #REDDIT
    elif service == Service.REDDIT:
        msg = f'''
Title: {track["title"]}
Summary: {track["summary"]}
Link: {track["stores"]["itch"]}
'''

    #YOUTUBE
    elif service == Service.YOUTUBE:
        msg = f'''
{track["summary"]}

homepage: https://ludoloon.studio/music#{track["url"]}
itch.io: https://ludoloonstudio.itch.io/{track["url"]}
Newgrounds: https://ludoloonstudio.newgrounds.com/audio
Patreon (get stems & tracks in advance): https://patreon.com/ludoloonstudio

{combine_tags(module.DEFAULT_TAGS, track["tags"], prepend="#")}
'''
    #SOUNDCLOUD
    elif service == Service.SOUNDCLOUD:
        #Uploads pass multiple files, pick one for now
        msg = f'''
Title: {track["title"]}
URL: {track["url"]}
License: Creative commons, allow sharealike

-----
Description:
-----

{track["summary"]}

Style: {combine_tags(track["tags"], separator=", ")}
BPM: {track["details"]["bpm"]}

--More Music--
Homepage: https://ludoloon.studio/music
Itch.io: {track["stores"]["itch"]}
Patreon (get stems & tracks in advance): https://patreon.com/ludoloonstudio

-----
Tags:  {combine_tags(module.DEFAULT_TAGS, track["tags"], separator=", ")}
'''

    #NEWGROUNDS
    elif service == Service.NEWGROUNDS:
        #Uploads pass multiple files, pick one for now
        msg = f'''
Title: {track["title"]}
Tagline: {track["summary"]}
License: Creative commons, allow sharealike

Classification: Soundtrack
-----
Description:
-----

{track["summary"]}

Format: .MP3 (VBR)
Style: {combine_tags(track["tags"], separator=", ")}
BPM: {track["details"]["bpm"]}

--More Music--
Homepage: https://ludoloon.studio/music
Itch.io: {track["stores"]["itch"]}
Patreon (get stems & tracks in advance): https://patreon.com/ludoloonstudio

-----
Tags:  {combine_tags(module.DEFAULT_TAGS, track["tags"], separator=", ")}
'''

    #ITCH.IO
    elif service == Service.ITCH:
        #Get the number of tracks before re-assigning release
        num_tracks = len(release.tracks)
        msg = f'''
Title: {track["title"]}
Tagline: {track["summary"]}
Youtube Video: {track["streaming"]["youtube"]}
Classification: Soundtrack

Description:
-----
<em>{track["summary"]}</em>

<h4>Technical Details</h4>
<ul>
<li><strong>License: Creative Commons International 4.0 Attribution (Royalty Free)</strong></li>
<li><strong>Number of tracks:</strong> {num_tracks}</li>
<li><strong>Format:</strong> .WAV <em>(44.1khz / 16-bit)</em> | .MP3 <em>(VBR)</em> / {track["details"]["loop"]} / Stereo</li>
<li><strong>Style:</strong> {combine_tags(track["tags"], separator=", ")} </li>
<li><strong>BPM:</strong> {track["details"]["bpm"]}</li>
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
Tags: {combine_tags(module.DEFAULT_TAGS, track["tags"], separator=", ")}

BG: #222
BG2: #333
Text: #eaeaea
Link: #2ce8f4
'''

    return msg