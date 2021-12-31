from PIL import Image, ImageDraw, ImageFont
import textwrap

class PhotoRender:
    texts = []
    image: Image.Image

    def __init__(self, config: dict):
        self.texts = config['texts']
        name = config['name']
        template_img = f'./templates/{name}/template.jpg'
        self.image = Image.open(path)

    def writeText(self, xy: tuple, width: int, font_filename: str, font_size: int, lw_multiplier: int, text: str):
        img_editable = ImageDraw.Draw(self.image)
        font_draw = ImageFont.truetype(font_filename, font_size)
        line_width = lw_multiplier * width/font_size
        text_lines = textwrap.fill(text, line_width)
        img_editable.text(xy, text_lines, (0,0,0), font=font_draw)

    def run(self, texts: list):
        # Check if JSON is OK
        if len(self.texts) > 0:
            for i in range(len(self.texts)):
                text_config = self.texts[i]
                if 'default' in text_config and i >= len(texts):
                    text = text_config["default"]
                else:
                    text = texts[i]
                font_filename = './fonts/DejaVuSans.ttf'
                if 'font_name' in text_config:
                    font_filename = f'./fonts/{text_config["font_name"]}.ttf'
                self.writeText(tuple(text_config["pos"]), text_config['img_width'], font_filename, text_config['font_size'], text_config['lw_multiplier'], text)

    def saveToDisk(self, path: str):
        """
        Save image to file
        """
        self.image.save(path, format='JPEG')

    def get(self) -> Image.Image:
        """
        Return image object
        """
        return self.image

    def cleanup(self):
        """
        Close all opened files
        """
        self.image.close()
