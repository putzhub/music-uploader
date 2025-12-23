# https://mastodonpy.readthedocs.io/en/stable/

from mastodon import Mastodon

USERCRED_FILE="secrets/masto_usercred.secret"
CLIENTCRED_FILE="secrets/masto_clientcred.secret"
SECRETS_FILE="secrets/mastocred.secrets"

# Register your app! This only needs to be done once (per server, or when
# distributing rather than hosting an application, most likely per device and server).
# Uncomment the code and substitute in your information:

def post(tracks, testing=False):
    #Initialize our vairables.
    client_id = ""
    client_secret = ""
    access_token = ""
    #Assume only one track for now
    track = tracks[0]

    with open(SECRETS_FILE) as f:
        client_id = f.readline()
        client_secret = f.readline()
        access_token = f.readline()

    # Then, log in. This can be done every time your application starts, or you can use the persisted information:
    mastodon = Mastodon(client_id, client_secret, access_token, api_base_url="https://mastodon.gamedev.place")
    
    msg = '''
{0}

{1}

#vgm #royaltyfree #asset #music
'''.format(track["summary"], track["embed"].replace("embed", "video"))

    if testing:
        print(msg)
    else:
        mastodon.toot(msg)
    
    #Successfully posted
    return True