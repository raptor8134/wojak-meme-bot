from PIL import Image
from io import BytesIO
from os import getenv
from dotenv import load_dotenv

def PILToBytes(img: Image.Image)-> bytes:
    """
    Convert PIL Image to bytes
    """
    buf = BytesIO()
    img.save(buf, format='JPEG')
    byte_im = buf.getvalue()
    buf.close()
    return byte_im

def checkEnv(envs: list):
    """
    Check if a list of enviroment variables are set, raise exception if not
    """
    for env in envs:
        if not getenv(env):
            raise Exception(f'{env} enviroment variable not found!')
