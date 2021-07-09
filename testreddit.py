#!/bin/python3
from praw import Reddit
from os import getenv

reddit = Reddit(  
    user_agent      = getenv("R_USER_AGENT"),
    client_id       = getenv("R_CLIENT_ID"),
    client_secret   = getenv("R_CLIENT_SECRET"),
    username        = getenv("R_USERNAME"),
    password        = getenv("R_PASSWORD")
)

comment = reddit.comment("h1lmfcz")

print("https://reddit.com" + comment.permalink)
print(comment.replies.list())
comment.refresh()
print(comment.replies.list())
