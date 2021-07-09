from imgur_python import Imgur
from os import path
from os import getenv
import PIL

def postimg(image, title, description):
    client = Imgur({
        "client_id":        getenv("I_CLIENT_ID"), 
        "client_secret":    getenv("I_CLIENT_SECRET")
    }) 

    if type(image) is PIL.JpegImagePlugin.JpegImageFile:
        image.save("/tmp/wojakimg.jpg")
        image = "/tmp/wojakimg.jpg"

    image = client.image_upload(path.realpath(image), title, description)
    url = "https://i.imgur.com/" + image["response"]["data"]["id"] + ".jpg"
    return url
