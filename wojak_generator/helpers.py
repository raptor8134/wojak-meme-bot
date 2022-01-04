from PIL.Image import Image
from io import BytesIO
from os import getenv
from wojak_generator.render.modes import modes

def PILToBytes(img: Image)-> bytes:
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

def isValidMode(mode: str)-> bool:
    if mode in modes:
        return True
    return False

def pickRender(mode: str, config: dict):
    return modes[mode](config)
