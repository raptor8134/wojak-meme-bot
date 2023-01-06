from PIL.Image import Image
from io import BytesIO
from os import getenv
from wojak_generator.render.modes import modes

def PIL_to_bytes(img: Image)-> bytes:
    """
    Convert PIL Image to bytes
    """
    with BytesIO() as buf:
        img.save(buf, format='JPEG')
        byte_im = buf.getvalue()
        return byte_im

def check_env(envs: list):
    """
    Check if a list of enviroment variables are set, raise exception if not
    """
    for env in envs:
        if not getenv(env):
            raise Exception(f'{env} enviroment variable not found!')

def pick_render(mode: str, config: dict):
    if mode in modes:
        return modes[mode](config)
    else:
        raise Exception('Mode not found')

