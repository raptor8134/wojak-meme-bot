from imgur_python import Imgur
from os import path
from os import getenv
import PIL

def postimg(image, title, description):
    client = Imgur({
        "client_id":        getenv("I_CLIENT_ID"), 
        "access_token":     getenv("I_CLIENT_ID"), 
        "client_secret":    getenv("I_CLIENT_SECRET")
    }) 

    if type(image) is PIL.JpegImagePlugin.JpegImageFile:
        title = description.replace(' ', '')
        image.save(f"/tmp/my_imgur_python/{title}.jpg")
        image = f"/tmp/my_imgur_python/{title}.jpg"

    image = client.image_upload(path.realpath(image), title, description)
    url = "https://i.imgur.com/" + image["response"]["data"]["id"] + ".jpg"
    return url
