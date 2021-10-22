from praw import Reddit
from praw.models import Submission, Subreddit, Comment
from time  import sleep
from os import getenv
import threading
import re

from imgur import *
from meme import *

def redditbot(memes, sub):

    botmsg = "\n\n ^([Github](https://github.com/raptor8134/wojak-meme-bot))"

    reddit = Reddit(
        user_agent      = getenv("R_USER_AGENT"),
        client_id       = getenv("R_CLIENT_ID"),
        client_secret   = getenv("R_CLIENT_SECRET"),
        username        = getenv("R_USERNAME"),
        password        = getenv("R_PASSWORD")
    )
    
    while True:
        comments = reddit.subreddit(sub).stream.comments()
        for comment in comments:
            c = comment.body
            if c.startswith("!") and c[1::] in memes:
                should_reply = True
                comment.refresh()
                for reply in comment.replies:
                    if reply.author.name == "wojak-meme-bot":
                        should_reply = False 
                        break
                if should_reply:
                    print("\033[1mFound a comment:\033[0m")
                    print("\thttps://reddit.com/" + comment.permalink)
                    try:
                        html = comment.parent().body_html
                    except:
                        html = "bruh" # do the post title if its a top level comment
                    text = re.sub("<[^<]+?>", "", html)
                #### IMPORTANT: THIS WILL FAIL IF YOU DO NOT PATCH TEXTWRAP
                #### In textwrap.py (in /usr/lib/python3.x/ if you installed it as root),
                #### change line 213 to `space_left = round(width - cur_len)`. 
                #### This prevents the typeError from happening because it will be an int
                #### I will submit a bug report later but this should work for now
                    meme = memes[c[1::]](text)
                    link = postimg(meme, "r/" + sub + " wojak meme", "")
                    reply = comment.reply("[Here's your meme!](" + link + ")" + botmsg)
                    print("\t\033[1;32m✓ Reply posted\033[0m")
