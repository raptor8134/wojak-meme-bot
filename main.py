#!/bin/python3
from sys import argv
from os import system, path, getenv
from multiprocessing import Process

from meme import *
from reddit import *
from discord import *

memes = {
    "!chadyes":     chadyes,
    "!chadno" :     chadno,
    "!soyjack":     angrysoyjack,
}

subreddits = [
    "wojakmemebot",
    "politicalcompassmemes",
    "196",
    "shitposting",
]

if argv[1] == "--reddit":
    for sub in subreddits:
        Process(target=redditbot, args=(memes, sub)).start()
elif argv[1] == "--discord":
    discordbot(memes)
else:
    memes[argv[1]](argv[2]).save("finishedmeme.jpg")
