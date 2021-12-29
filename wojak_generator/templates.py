import json
from os.path import isdir

class Templates:
    base = './templates'
    memes = []

    def __init__(self):
        f = open(self.base + '/list.json')
        list_string = f.read()
        self.memes = json.loads(list_string)
        f.close()

    def all(self)-> list:
        """
        Return all templates (Useful for bots like Reddit or Discord)
        """
        items = []
        for meme in self.memes:
            items.append(self.one(meme))
        return items

    def one(self, meme: str)-> dict:
        """
        Return just one template
        """
        path = f'{self.base}/{meme}'
        if isdir(path):
            # Import JSON config
            f = open(path + "/config.json")
            config_string = f.read()
            config = json.loads(config_string)
            f.close()
            return config
        raise Exception('Template not found')
