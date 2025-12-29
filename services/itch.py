import webbrowser
import services

DEFAULT_TAGS = ["royalty-free", "music", "asset-pack", "indie", "wav"]

def upload(json):
    '''Prep copy & paste material for itch.io, grab url when done.'''
    #Get our copy & paste message
    print(services.prep_post(json, services.Service.ITCH))

    #Open relevant pages and post
    webbrowser.open("https://itch.io/game/new")
    itch_url = input("What is the project URL on itch.io?")
    webbrowser.open("https://itch.io/category/10022/new-topic")
    input("Did you create an itch forum post yet? (MAKE SURE ITCH PAGE IS READY FIRST!) [Press Enter]")
    return itch_url