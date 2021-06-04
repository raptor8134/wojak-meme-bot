#!/bin/python3
from PIL import Image, ImageFont, ImageDraw # pillow on pip

def angrysoyjack(text):
    soyimg = Image.open("angrysoyjack.jpg")
    font = ImageFont.truetype("/usr/share/fonts/DejaVuSans.ttf")
    print(text)
