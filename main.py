#!/bin/python3
from sys import argv
from os import system, path, getenv

from meme import *
from reddit import *
from discord import *

memes = {
    "chadyes":      chadyes,
    "chadno":       chadno,
    "angrysoyjack": angrysoyjack,
}

subreddits = [
#    "wojakmemebot",
    "politicalcompassmemes",
#    "196",
#    "shitposting",
]

if argv[1] == "--reddit":
    redditbot(memes, subreddits)
elif argv[1] == "discord":
    discordbot(memes)
else:
    memes[argv[1]](argv[2]).save("finishedmeme.jpg")
