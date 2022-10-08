from PIL import Image
from io import BytesIO


def crop_image(image_path: str, cut_to=(500, 500)):
    """Makes image's thumbnail bt given parameters. By default, crops to 500x500"""
    img = Image.open(image_path)
    blob = BytesIO()

    try:
        img.thumbnail(cut_to, Image.ANTIALIAS)
    except IOError:
        print("Can't crop")

    img.save(blob, "PNG")
    return blob
