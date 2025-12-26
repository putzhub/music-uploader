# https://docs.bsky.app/docs/advanced-guides/
#TODO: Refer to this doc to get embeds (hopefully) working
#https://github.com/MarshalX/atproto/blob/main/examples/advanced_usage/send_embed.py

from atproto import Client, client_utils, models, exceptions
from getpass import getpass
from PIL import Image
import webbrowser

SECRETS_FILE = "secrets/bluesky.secrets"

def request_credentials(msg="Requesting login credentials"):
    print(msg)
    with open(SECRETS_FILE, "w") as f:
        login = input("Full Handle:")
        password = getpass("App Password: ")
        f.writelines([login + "\n", password])
    
    return login, password

def post(summary, embed, tags, testing=False):
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

    print(msg)
    webbrowser.open("https://bsky.app")
    input("Welp, did ya post it to bluesky? [press enter]")
    return True

def wastetime(title, summary, embed, tags, cover, testing=False, artist="LudoLoon Studio"):
    if embed == "" or embed is None or summary == "" or summary is None:
        #Don't bother posting without a video
        print("No video or summary, not posting to Mastodon")
        return False
    
    #Initialize our vairables.
    login = ""
    password = ""
    try:
        with open(SECRETS_FILE) as f:
            login = f.readline().strip()
            password = f.readline().strip()
    except FileNotFoundError:
        login, password = request_credentials("Bluesky - Login for the first time.")

    #Login
    client = Client()
    try:
        client.login(login=login, password=password)
    except exceptions.UnauthorizedError:
        login, password = request_credentials("Login unsuccessful, try again.")

    #Prep message
    #TODO probably have the message  written elsewhere or brought in as an arg
    post_tags = ["music", "gameaudio", "vgm", "bgm", "royaltyfree", 
            "indie", "gamemusic"]
    for tag in tags:
        post_tags.append(tag)
    #give 'em hashtags and remove spaces for description
    post_tags = ["#"+str(tag).replace(" ", "") for tag in post_tags]
    #post_tags = " ".join(post_tags)

    #Bluesky uses some weird text builder shit.
    msg = client_utils.TextBuilder().text(summary)
    for tag in post_tags:
        msg.tag(" " + tag, tag.replace("#",""))
    msg.link("Youtube Link", embed)
    
    img_data = Image.open(cover).resize((256,256)).tobytes()
    uploaded_blob = client.upload_blob(img_data).blob
    uploaded_blob.mime_type = "image/*"

    embed_external = models.AppBskyEmbedExternal.Main(
        external=models.AppBskyEmbedExternal.External(
            title=title,
            uri=embed,
            alt='Music by ' + artist,
        )
    )

    if not testing:
        client.send_post(msg, embed=embed_external)

    #Successfully posted
    return True