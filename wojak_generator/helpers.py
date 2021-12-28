from PIL import Image
from io import BytesIO

def PILToBytes(img: Image.Image)-> bytes:
    buf = BytesIO()
    img.save(buf, format='JPEG')
    byte_im = buf.getvalue()
    buf.close()
    return byte_im
