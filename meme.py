from PIL import Image, ImageFont, ImageDraw
import textwrap

def makememe (image, text, xy, width, fontsize=60, font="/usr/share/fonts/TTF/DejaVuSans.ttf", line_width_multiplier=1):
    if type(image) is str: 
        img = Image.open(image) # if we pass a path, open it
    else:
        img = image # if we pass an image object, use it
    img_editable = ImageDraw.Draw(img)
    font_draw = ImageFont.truetype(font, fontsize)
    line_width = line_width_multiplier * width/fontsize
    text_lines = textwrap.fill(text, line_width)
    img_editable.text(xy, text_lines, (0,0,0), font=font_draw)
    return img

def angrysoyjack (text, image="img/angrysoyjack.jpg"):
    img = makememe(image, text, (680,70), 960, 50)
    return img

def chadyes (text, text2="Yes.", image="img/chadyes.jpg"):
    img = makememe(image, text, (60,760), 550, 40, "/usr/share/fonts/TTF/Impact.TTF", 2.5)
    if len(text2) < 6:
        fontsize = 100
        x = 1100
    else:
        fontsize = 60
        x = 950
    img = makememe(img, text2, (x,740), 400, fontsize, "/usr/share/fonts/TTF/Impact.TTF")
    return img

def chadno(text, text2="No."):
    img = chadyes(text, text2)
    return img

