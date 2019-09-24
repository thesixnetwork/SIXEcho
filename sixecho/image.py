import base64
import hashlib
import json
import os

import imagehash
from PIL import Image as M
from PIL.ExifTags import TAGS


def convert_to_string(value):
    str_type = type(value).__name__
    if str_type == "bytes":
        return value.decode("UTF-8", errors='replace')
    elif str_type == "tuple":
        return str(value)
    elif str_type == "str":
        return value
    elif str_type == "int":
        return value
    elif str_type == "dict":
        return str(value)
    else:
        return "con not file" + str_type


class Image(object):
    """
    client class 
    """
    def __init__(self):
        """
        Args:

        """
        self.sha256 = ""
        self.file_size = 0
        self.type = "IMAGE"
        self.meta_media = {}
        self.exif = {}
        self.digest = ""

    def set_meta(self, meta_media):
        """
        Args:
        meta_media - Required meta media
            name - Required : picture name

        """
        self.meta_media = meta_media

    def merge_meta(self, meta_media):
        meta_media.update(self.exif)
        self.meta_media = meta_media

    def generate(self, imgpath=None):
        """
        Args:
        imgpath - Required
        """
        sha256 = hashlib.sha256()
        with open(imgpath, "rb") as image:
            b64string = base64.b64encode(image.read())
        sha256.update(b64string)
        self.sha256 = sha256.hexdigest()
        ob_img = M.open(imgpath)
        average_hash = imagehash.average_hash(ob_img)
        phash = imagehash.phash(ob_img)
        dhash = imagehash.dhash(ob_img)
        whash = imagehash.whash(ob_img)
        self.file_size = os.path.getsize(imgpath)
        self.digest = str(average_hash) + "," + str(phash) + \
            "," + str(dhash) + "," + str(whash)
        info = ob_img._getexif()
        ret = {}
        try:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = convert_to_string(value)
                self.exif = ret
        except:
            print("Error read meta")
