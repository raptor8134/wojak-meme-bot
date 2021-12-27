from imgur_python import Imgur
from os import getenv, remove
import PIL

def postimg(image, title, description):
    client = Imgur({
        "client_id":        getenv("I_CLIENT_ID"), 
        "access_token":     getenv("I_CLIENT_ID"), 
        "client_secret":    getenv("I_CLIENT_SECRET")
    }) 

    if type(image) is PIL.JpegImagePlugin.JpegImageFile:
        path = "/tmp/my_imgur_python/"+title.replace(' ', '').replace('/','')+".jpg"
        image.save(path)
        image = path

    image = client.image_upload(image, title, description)
    url = "https://i.imgur.com/" + image["response"]["data"]["id"] + ".jpg"
    #remove(path)
    return url
