# https://mastodonpy.readthedocs.io/en/stable/

from mastodon import Mastodon

USERCRED_FILE="secrets/masto_usercred.secret"
CLIENTCRED_FILE="secrets/masto_clientcred.secret"
SECRETS_FILE="secrets/mastocred.secrets"

# Register your app! This only needs to be done once (per server, or when
# distributing rather than hosting an application, most likely per device and server).
# Uncomment the code and substitute in your information:

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

    with open(SECRETS_FILE) as f:
        client_id = f.readline()
        client_secret = f.readline()
        access_token = f.readline()

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
        print(msg)
    else:
        mastodon.toot(msg)
    
    #Successfully posted
    return True