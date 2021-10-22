###### TODO: clean up long function arguments, they're really annoying
from PIL import Image, ImageFont, ImageDraw
import textwrap

def makememe(image, text, xy, width, fontsize=60,
             font="fonts/DejaVuSans.ttf", lw_multiplier=1):
    if type(image) is str: 
        img = Image.open(image) # if we pass a path, open it
    else:
        img = image # if we pass an image object, use it
    img_editable = ImageDraw.Draw(img)
    font_draw = ImageFont.truetype(font, fontsize)
    line_width = lw_multiplier * width/fontsize
    text_lines = textwrap.fill(text, line_width)
    img_editable.text(xy, text_lines, (0,0,0), font=font_draw)
    return img

def angrysoyjack(text, image="img/angrysoyjack.jpg"):
    return makememe(image, text, (680,70), 960, 50)

def chadyes(text, text2="Yes.", image="img/chadyes.jpg"):
    img = makememe( image, text, (60,760), 550, 40,
                    font="fonts/Impact.ttf", lw_multiplier=2.5)
    if len(text2) < 6:
        fontsize = 100
        x = 1100
    else:
        fontsize = 60
        x = 950
    img = makememe( img, text2, (x,740), 400, fontsize, 
                    font="fonts/Impact.ttf")
    return img

def chadno(text, text2="No."):
    return chadyes(text, text2)

def gigachad(text):
    return makememe("img/gigachad.jpg", text, (20,780), 620, lw_multiplier=2.5,
                    font="fonts/Impact.ttf", fontsize=40)
