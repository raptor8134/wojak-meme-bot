import textwrap

class AsciiRender:
    texts = []
    template = ''
    out = ''

    def __init__(self, config: dict):
        self.texts = config['texts']
        name = config['name']
        template_txt = f'./templates/{name}/template.txt'
        with open(template_txt) as f:
            self.template = f.read()

    def writeText(self, text: str, index: int, width: int):
        wrapped_text = textwrap.fill(text, width=width)
        if not self.out:
            self.out = self.template.replace(f'TEXT{index}_HERE', wrapped_text)
        else:
            self.out = self.out.replace(f'TEXT{index}_HERE', wrapped_text)

    def run(self, texts: list):
        if len(self.texts) > 0:
            for i in range(len(self.texts)):
                text_config = self.texts[i]
                if 'default' in text_config and i >= len(texts):
                    text = text_config["default"]
                else:
                    text = texts[i]
                self.writeText(text, i + 1, text_config['ascii_width'])

    def saveToDisk(self, path: str):
        """
        Save text to disk
        """
        with open(path, 'w') as f:
            f.write(self.out)

    def get(self):
        """
        Get output
        """
        return self.out

    def cleanup(self):
        pass
