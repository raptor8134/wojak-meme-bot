import praw
from os import getenv, system

os.system(". ./redditlogin.sh")

bot = praw.Reddit(  
    user_agent = getenv("R_USER_AGENT"),
    client_id = getenv("R_CLIENT_ID"),
    client_secret = getenv("R_CLIENT_SECRET"),
    username = getenv("R_USERNAME"),
    password = getenv("R_PASSWORD"))

def gettargets ():
    None
    
