import requests
from os import getenv
from wojak_generator.helpers import PIL_to_bytes

class Uploader:
    BASE_URL = 'https://api.imgur.com/3/upload'
    s = requests.Session()
    error = ''

    def __init__(self, client_id: str):
        self.s.headers['Authorization'] = f'Client-ID {client_id}'

    def send(self, img, title: str, description: str)-> str:
        self.error = ''
        # Get image bytes first
        byte_im = PIL_to_bytes(img)
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

        # Rate Limited
        # TODO, CHECK ALL POSIBILITIES
        if res.headers['X-POST-Rate-Limit-Remaining'] == 0:
            time_remaining = res.headers['X-Post-Rate-Limit-Reset'] / 60
            self.error = f'Imgur Rate Limit! Please wait {time_remaining} minutes and try again'
        else:
            self.error = 'Unknown Imgur error, please try again later'
        return ''
