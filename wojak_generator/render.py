from PIL import Image, ImageDraw, ImageFont
import textwrap

class PhotoRender:
    config = {}
    image: Image.Image

    def __init__(self, path: str, config: dict):
        self.config = config
        self.image = Image.open(path)

    def get_text_size(self, font_filename, font_size, text):
        font = ImageFont.truetype(font_filename, font_size)
        return font.getsize(text)

    def get_font_size(self, text, font, max_width=None, max_height=None):
        if max_width is None and max_height is None:
            raise ValueError('You need to pass max_width or max_height')
        font_size = 1
        text_size = self.get_text_size(font, font_size, text)
        if (max_width is not None and text_size[0] > max_width) or \
           (max_height is not None and text_size[1] > max_height):
            raise ValueError("Text can't be filled in only (%dpx, %dpx)" % \
                    text_size)
        while True:
            if (max_width is not None and text_size[0] >= max_width) or \
               (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            font_size += 1
            text_size = self.get_text_size(font, font_size, text)

    def writeText(self, xy: tuple, wh: tuple, font_filename: str, text: str):
        # Get appropiate font size
        font_size = self.get_font_size(text, font_filename, wh[0], wh[1])
        # Create font with needed size
        font = ImageFont.truetype(font_filename, font_size)
        # Create string from textwrap
        text_lines = '\n'.join(textwrap.wrap(text, wh[0]))
        # Create empty image with 10px of margin and paste text on it
        container_img = Image.new('RGB', (wh[0] + 10, wh[1] + 10), (255,255,255))
        container_draw = ImageDraw.Draw(container_img)
        container_draw.text((0, 0), text_lines, font=font, fill='black')
        self.image.paste(container_img, xy)

    def run(self, texts: list):
        # Check if JSON is OK
        if 'texts' in self.config:
            for i in range(len(self.config["texts"])):
                text_config = self.config["texts"][i]
                if 'default' in text_config:
                    text = text_config["default"]
                else:
                    text = texts[i]
                font_filename = './fonts/DejaVuSans.ttf'
                if 'font' in text_config:
                    font_filename = f'./fonts/{text_config["font"]}.ttf'
                self.writeText(tuple(text_config["pos"]), tuple(text_config["size"]), font_filename, text)

    def saveToDisk(self, file: str):
        self.image.save(file, format='JPEG')

    def getImage(self)-> Image.Image:
        return image

    def cleanup(self):
        self.image.close()
