# https://mastodonpy.readthedocs.io/en/stable/

from mastodon import Mastodon, errors
from getpass import getpass

SECRETS_FILE="secrets/mastocred.secrets"

def request_credentials(msg="Requesting login credentials"):
    print(msg)
    with open(SECRETS_FILE, "w") as f:
        client_id = getpass("Client ID:")
        client_secret = getpass("Client Secret: ")
        access_token = getpass("Your Access Token: ")
        f.writelines([client_id + "\n", client_secret + "\n", access_token + "\n"])
    
    return client_id, client_secret, access_token

def post(summary, embed, tags, testing=False):
    if embed == "" or embed is None or summary == "" or summary is None:
        #Don't bother posting without a video
        print("No video or summary, not posting to Mastodon")
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
    #TODO probably have the message  written elsewhere or brought in as an arg
    post_tags = ["music", "asset", "gameaudio", "vgm", "bgm", "royaltyfreemusic", 
          "soundtrack", "indie", "renoise", "composer", "game", "videogame",
          "gamemusic", "ost", "pack", "bundle"]
    for tag in tags:
        post_tags.append(tag)
    #give 'em hashtags and remove spaces for description
    post_tags = [str("#"+tag).replace(" ", "") for tag in post_tags]
    post_tags = " ".join(post_tags)

    msg = '''
{0}

{1}

{2}
'''.format(summary, embed, post_tags)

    if testing:
        #Make sure we can login successfully if testing. Must have profile scope.
        mastodon.account_verify_credentials()
        #Make sure the message is what we expect
        print(msg)
    else:
        mastodon.toot(msg)
    
    #Successfully posted
    return True