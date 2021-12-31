from PIL import Image, ImageDraw, ImageFont
import textwrap

class PhotoRender:
    config = {}
    image: Image.Image

    def __init__(self, path: str, config: dict):
        self.config = config
        self.image = Image.open(path)

    def writeText(self, xy: tuple, width: int, font_filename: str, font_size: int, lw_multiplier: int, text: str):
        img_editable = ImageDraw.Draw(self.image)
        font_draw = ImageFont.truetype(font_filename, font_size)
        line_width = lw_multiplier * width/font_size
        text_lines = textwrap.fill(text, line_width)
        img_editable.text(xy, text_lines, (0,0,0), font=font_draw)

    def run(self, texts: list):
        print(texts)
        # Check if JSON is OK
        if 'texts' in self.config:
            for i in range(len(self.config["texts"])):
                text_config = self.config["texts"][i]
                if 'default' in text_config and i >= len(texts):
                    text = text_config["default"]
                else:
                    text = texts[i]
                font_filename = './fonts/DejaVuSans.ttf'
                if 'font_name' in text_config:
                    font_filename = f'./fonts/{text_config["font_name"]}.ttf'
                self.writeText(tuple(text_config["pos"]), text_config['width'], font_filename, text_config['font_size'], text_config['lw_multiplier'], text)

    def saveToDisk(self, file: str):
        """
        Save image to file
        """
        self.image.save(file, format='JPEG')

    def getImage(self) -> Image.Image:
        """
        Return image object
        """
        return self.image

    def cleanup(self):
        """
        Close all opened files
        """
        self.image.close()
