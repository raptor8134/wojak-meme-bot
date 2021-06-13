#!/bin/python3
from sys import argv
from os import system, path

from meme import *
from reddit import *
from discord import *

# Hacky and temporary, TODO add option parser
#eval(argv[1] + "(" + "\"" + argv[2]+ "\"" +").save(\"finishedmeme.jpg\")")

memes = {
    "chadyes":      chadyes,
    "chadno":       chadno,
    "angrysoyjack": angrysoyjack,
}

opts = {
    "--reddit":     redditbot,
    "--discord":    discordbot,
}

#system(". " + path.realpath("./login.sh"))

for opt in opts:
    if opt in argv[1]:
        opts[opt](memes)
    else:
        for meme in memes:
            if meme in argv[1]:
                memes[meme](" ".join(argv[2::]))
