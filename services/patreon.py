import webbrowser

def post(release, testing=False):
    #Release is unused but helps maintain paradigm consistency

    webbrowser.open("https://patreon.com")
    input("Don't forget to post to patreon on appropriate posts [Press enter]")
    return True