from imgur_python import Imgur
from os import system, getenv, path

system(". ./imgurlogin.sh")

def postimg(image, title, description):
    client = Imgur({
        "client_id":        getenv("I_CLIENT_ID"), 
        "client_secret":    getenv("I_CLIENT_SECRET")
    }) 
    image = imgur_client.image_upload(path.realpath(image), title, description)
    url = image["response"]["data"]["id"]
    return url
