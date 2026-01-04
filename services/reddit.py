import webbrowser
import services

def post(release, testing=False):
    '''Prepare a message to copy & paste onto bluesky for promotion.'''
    print(services.prep_post(release, services.Service.REDDIT))
    webbrowser.open("https://www.reddit.com/r/gameassets/")
    webbrowser.open("https://www.reddit.com/r/freegameassets/")
    webbrowser.open("https://www.reddit.com/r/itchio/")
    input("Welp, did ya post it to reddit? [press enter]")
    return True

#Uncomment this if I ever wanna try using the reddit api someday.
'''
import praw
from getpass import getpass

SECRETS_FILE="secrets/reddit.secrets"

def request_credentials(msg="Requesting login credentials"):
    print(msg)
    with open(SECRETS_FILE, "w") as f:
        client_id = getpass("Client ID:")
        client_secret = getpass("Client Secret: ")
        username = input("")
        f.writelines([client_id + "\n", client_secret + "\n", username + "\n"])
    
    return client_id, client_secret, username

def post(release, testing=False):
    try:
        with open(SECRETS_FILE) as f:
            client_id = f.readline()
            client_secret = f.readline()
            username = f.readline()
    except FileNotFoundError:
        client_id, client_secret, username = request_credentials("Reddit - first time login.")

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        password=getpass("Reddit Password:"),
        user_agent="Muisc-Uploader.py",
        username=username,
    )
'''