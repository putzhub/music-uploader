# https://mastodonpy.readthedocs.io/en/stable/

from mastodon import Mastodon

USERCRED_FILE="secrets/masto_usercred.secret"
CLIENTCRED_FILE="secrets/masto_clientcred.secret"
SECRETS_FILE="secrets/mastocred.secrets"

# Register your app! This only needs to be done once (per server, or when
# distributing rather than hosting an application, most likely per device and server).
# Uncomment the code and substitute in your information:

def post(summary, embed, testing=False):
    if embed is "" or embed is None or summary is "" or summary is None:
        #Don't bother posting without a video
        print("no video or summary")
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
    
    msg = '''
{0}

{1}

#vgm #royaltyfree #asset #music
'''.format(summary, embed)

    if testing:
        print(msg)
    else:
        mastodon.toot(msg)
    
    #Successfully posted
    return True