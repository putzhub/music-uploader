# https://mastodonpy.readthedocs.io/en/stable/

from mastodon import Mastodon, errors
from getpass import getpass
import services
import logging

logger = logging.getLogger(__name__)

SECRETS_FILE="secrets/mastocred.secrets"
DEFAULT_TAGS = ["music", "asset", "gameaudio", "vgm", "bgm", "royaltyfreemusic", 
          "soundtrack", "indie", "renoise", "composer", "game", "videogame",
          "gamemusic", "ost", "pack", "bundle"]

def request_credentials(msg="Requesting login credentials"):
    print(msg)
    with open(SECRETS_FILE, "w") as f:
        client_id = getpass("Client ID:")
        client_secret = getpass("Client Secret: ")
        access_token = getpass("Your Access Token: ")
        f.writelines([client_id + "\n", client_secret + "\n", access_token + "\n"])
    
    return client_id, client_secret, access_token

def post(release, testing=False):
    #Only use first track's meta data
    track = release.tracks[0]

    #Don't bother posting without a video
    if "embed" not in track or "summary" not in track:
        logger.error("No video or summary, not posting to Mastodon")
        return False
    
    #Initialize our vairables.
    client_id = ""
    client_secret = ""
    access_token = ""
    #Assume only one track for now

    try:
        with open(SECRETS_FILE) as f:
            client_id = f.readline()
            client_secret = f.readline()
            access_token = f.readline()
    except FileNotFoundError:
        client_id, client_secret, access_token = request_credentials("Mastodon - first time login.")
            
    # Then, log in. This can be done every time your application starts, or you can use the persisted information:
    mastodon = Mastodon(client_id, client_secret, access_token, api_base_url="https://mastodon.gamedev.place")

    #Prep message
    msg = services.prep_post(release, services.Service.BSKY)

    if testing:
        #Make sure we can login successfully if testing. Must have profile scope.
        mastodon.account_verify_credentials()
        #Make sure the message is what we expect
        print(msg)
    else:
        mastodon.toot(msg)
    
    #Successfully posted
    return True