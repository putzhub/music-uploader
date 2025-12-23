#  https://www.geeksforgeeks.org/python/using-python-to-post-stories-on-instagram/
'''
from instabot import Bot
from getpass import getpass

def post(summary, video, tags, testing=False):
    if video == "" or video is None or summary == "" or summary is None:
        #Don't bother posting without a video
        print("No video or summary, not posting to Instagram")
        return False

    #Initialize our vairables.
    bot = Bot("secrets/config/")
    bot.login(username="ludoloonstudio", password=getpass(prompt="Password: "))
    
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

    msg = ''.format(summary, post_tags)

    if testing:
        print(msg)
        print(video)
    else:
        id = bot.upload_video(video, msg)
        bot.upload_story_photo(upload_id=id)
    
    #Successfully posted
    bot.logout()
    return True
'''