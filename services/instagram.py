import webbrowser

def post(summary, tags, testing=False):
    '''Create an easy message to copy and paste for instagram.'''

    #testing bool is unused here but use it in the future if we ever connect to the api
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

See link in bio for more.

{1}
'''.format(summary, post_tags)

    print(msg)
    webbrowser.open("https://instagram.com")
    input("Welp, did ya post it to instagram? [press enter]")
    return True