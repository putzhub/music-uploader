from enum import Enum

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

def prep_post(release, service):
    msg = ""
    module = service.value

    #MASTODON
    if service == Service.MASTODON:
        msg = '''
{0}

{1}

{2}
'''.format(release["summary"], 
           release["streaming"]["youtube"], 
           combine_tags(module.DEFAULT_TAGS, release["tags"], prepend="#"))
    #INSTAGRAM
    elif service == Service.INSTAGRAM:
        msg = '''
{0}

See link in bio for more.

{1}
'''.format(release["summary"], 
           combine_tags(module.DEFAULT_TAGS, release["tags"], prepend="#"))

    return msg