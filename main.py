#!/bin/python3

from meme import *
from imgur import *
from reddit import *
from sys import argv

# Hacky and temporary, TODO add option parser
eval(argv[1] + "(" + "\"" + argv[2]+ "\"" +").save(\"finishedmeme.jpg\")")

 """
 # use thist later

 while True:
    comments = getcommments()
    for comment in comments: 
        # do stuff
        postimg(image)
 """
