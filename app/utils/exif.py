from PIL import Image
from PIL.ExifTags import TAGS


def extract_exif(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()

    if not exif_data:
        return None

    exif = {}
    for tag, value in exif_data.items():
        decoded = TAGS.get(tag, tag)
        exif[decoded] = value

    return exif