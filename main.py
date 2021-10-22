#!/bin/python3
from sys import argv, stderr
from os import system, path, getenv
from multiprocessing import Process
from time import ctime as time

from meme import *
from reddit import *
from discord_bot import *

memes = {
    "chadyes":     chadyes,
    "chadno":      chadno,
    "soyjack":     angrysoyjack,
    "gigachad":    gigachad,
}

subreddits = [
    "wojakmemebot",
    "politicalcompassmemes",
    "196",
    "shitposting",
    "u_raptor8134"
]


if argv[1] == "--reddit":
    print("Run on", time())
    for sub in subreddits:
        Process(target=redditbot, args=(memes, sub)).start()
        print("Started bot on r/" + sub)
elif argv[1] == "--discord":
    discordbot(memes)
elif argv[1] == "--discord-url":
    bot_url()
else:
    try:
        memes[argv[1]](" ".join(argv[2::])).save("finishedmeme.jpg")
    except:
        stderr.write("Error: unknown option\n")
