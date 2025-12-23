# https://docs.bsky.app/docs/advanced-guides/
#TODO: Refer to this doc to get embeds (hopefully) working
#https://github.com/MarshalX/atproto/blob/main/examples/advanced_usage/send_embed.py

from atproto import Client, client_utils, models

SECRETS_FILE = "secrets/bluesky.secrets"

def post(summary, embed, tags, testing=False):
    if embed == "" or embed is None or summary == "" or summary is None:
        #Don't bother posting without a video
        print("No video or summary, not posting to Mastodon")
        return False
    
    #Initialize our vairables.
    login = ""
    password = ""
    with open(SECRETS_FILE) as f:
        login = f.readline().strip()
        password = f.readline().strip()

    #Login
    client = Client()
    client.login(login=login, password=password)

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
    
    #embed_external = models.AppBskyEmbedRecordWithMedia.Main(
    #    video=models.AppBskyEmbedVideo.Main(
    #        video=embed,
    #        alt='Youtube video',
    #    )
    #)

    if testing:
        print(msg)
    else:
        client.send_post(msg)

    #Successfully posted
    return True