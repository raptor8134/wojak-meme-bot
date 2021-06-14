from praw import Reddit
from praw.models import Submission, Subreddit, Comment
from os import getenv
import re

from imgur import *
from meme import *

def __bot__(memes, subreddit):

    botmsg = "\n\n ^([Github](https://github.com/raptor8134/wojak-meme-bot) | [subreddit](https://reddit.com/r/r/wojakmemebot))"

    reddit = Reddit(  
        user_agent      = getenv("R_USER_AGENT"),
        client_id       = getenv("R_CLIENT_ID"),
        client_secret   = getenv("R_CLIENT_SECRET"),
        username        = getenv("R_USERNAME"),
        password        = getenv("R_PASSWORD")
    )
    
    sub = reddit.subreddit(subreddit)
    for comment in sub.stream.comments():
        if comment.body == "!soyjack":
            should_reply = True
            comment.refresh()
            for reply in comment.replies:
                if reply.author.name == "wojak-meme-bot":
                    should_reply = False 
                    break
            if should_reply:
                try: html = comment.parent().body_html
                except: html = "bruh" # do the post title if its a top level comment
                text = re.sub("<[^<]+?>", "", comment.parent().body_html)
            #### IMPORTANT: THIS WILL FAIL IF YOU DO NOT PATCH TEXTWRAP
            #### In textwrap.py (in /usr/lib/python3.x/ if you installed it as root),
            #### go to line 213 and put a `round()` function around `width - cur_len`. 
            #### This prevents the typeError from happening because it will be an int
            #### I will submit a bug report later but this should work for now
                meme = angrysoyjack(text)
                link = postimg(meme, "r/" + subreddit + " wojak meme", "")
                comment.reply("[Here's your meme!](" + link + ")" + botmsg)

def redditbot(memes):
    subreddits = [
        "wojakmemebot"
#        "politicalcompassmemes",
#        "196",
#        "shitposting",
]
    while True:
        __bot__(memes, subreddits[0])
