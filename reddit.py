from praw import Reddit
from praw.models import Submission, Subreddit, Comment
from os import getenv, system

from imgur import *
from meme import *

def __bot__(memes, subreddits):

    botmsg = "\n ^([Github](https://github.com/raptor8134/wojak-meme-bot) | [subreddit](https://reddit.com/r/r/wojakmemebot))"

    system(". ./redditlogin.sh")

    reddit = Reddit(  
        user_agent      = getenv("R_USER_AGENT"),
        client_id       = getenv("R_CLIENT_ID"),
        client_secret   = getenv("R_CLIENT_SECRET"),
        username        = getenv("R_USERNAME"),
        password        = getenv("R_PASSWORD")
    )
    
    sub = reddit.subreddit(sub)
    for comment in sub.stream.comments():
        #### IMPORTANT: THIS WILL FAIL IF YOU DO NOT PATCH TEXTWRAP
        #### In textwrap.py (in /usr/lib/python3.x/ if you installed it as root),
        #### go to line 213 and put a `round()` function around `width - cur_len`. 
        #### This prevents the typeError from happening because it will be an int
        #### I will submit a bug report later but this should work for now
        if comment.body == "!soyjack":
            meme = angrysoyjack(comment.parent().body)

def redditbot(memes):
    subreddits = [
#        "politicalcompassmemes",
#        "196",
#        "shitposting",
        "wojakmemebot"
    ]
    while True:
        __bot__(memes, subreddits)
