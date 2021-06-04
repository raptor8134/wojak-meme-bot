#!/bin/python3

from PIL import Image, ImageFont, ImageDraw
import textwrap

def makememe (image, text: str, xy: tuple, width: int, fontsize=60, font="/usr/share/fonts/DejaVuSans.ttf"):
    if type(image) is str: 
        img = Image.open(image) # if we pass a path, open it
    else:
        img = image # if we pass an image object, use it
        
    img_editable = ImageDraw.Draw(img)
    font_draw = ImageFont.truetype(font, fontsize)

    line_width = 1/fontsize * width
    text_lines = textwrap.fill(text, line_width)

    img_editable.text(xy, text_lines, (0,0,0), font=font_draw)

    return img

def angrysoyjack (text):
    makememe("img/angrysoyjack.jpg", text, (680,70), 960).save("finishedmeme.jpg")

def chadyes (text, text2="Yes"):
    img = makememe("img/chadyes.jpg", text, (0,0), 0, 0)
    makememe(img, text2, (0,0), 0, 0)

def chadno(text, text2="No"):
    chadyes(text, text2)

