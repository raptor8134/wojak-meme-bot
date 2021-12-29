import requests
from os import getenv
from wojak_generator.helpers import PILToBytes

class Uploader:
    BASE_URL = 'https://api.imgur.com/3/upload'
    s = requests.Session()

    def __init__(self):
        self.s.headers['Authorization'] = f'Client-ID {getenv("I_CLIENT_ID")}'

    def send(self, img, title: str, description: str)-> str:
        # Get image bytes first
        byte_im = PILToBytes(img)
        files = {
            'image': byte_im
        }
        body = {
            'type': 'file',
            'title': title,
            'description': description
        }
        res = self.s.post(self.BASE_URL, files=files, data=body)
        if res.ok:
            res_json = res.json()
            return res_json['data']['link']
        return ''
