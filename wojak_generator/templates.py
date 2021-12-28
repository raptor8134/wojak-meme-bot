import json
from os.path import isdir

class Templates:
    base = './templates'
    items = []

    def __init__(self):
        f = open(self.base + '/list.json')
        list_string = f.read()
        self.items = json.loads(list_string)
        f.close()

    def all(self)-> list:
        return self.items

    def one(self, wojak: str)-> dict:
        path = f'{self.base}/{wojak}'
        if isdir(path):
            # Import JSON config
            f = open(path + "/config.json")
            config_string = f.read()
            config = json.loads(config_string)
            f.close()
            return config
        raise Exception('Template not found')
