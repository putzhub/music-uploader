#LudoLoon Studio
from pathlib import Path
from os import getcwd

#hard code this since it's my own website anyway
WEBSITE_DIR = Path("/home/pootz/Documentos/Websites/LudoLoon Studio/ludoloon.studio")
IMAGE_DIR = Path(WEBSITE_DIR, "content/images/covers/")

def post(release):
    print(getcwd())