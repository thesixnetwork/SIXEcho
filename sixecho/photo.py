import base64
import hashlib
import os

import imagehash
from PIL import Image as M


class Image(object):
    """
    client class 
    """
    def __init__(self):
        """
        Args:

        """
        self.sha256 = ""
        self.average_hash = ""
        self.phash = ""
        self.dhsah = ""
        self.whash = ""
        self.file_size = 0
        self.type = "IMAGE"
        print("xxx")

    def set_meta(self, meta_media):
        """
        Args:
        meta_media : Required
        """
        print("xxx")

    def generate_img(self, imgpath=None):
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
        self.average_hash = imagehash.average_hash(ob_img)
        self.phash = imagehash.phash(ob_img)
        self.dhsah = imagehash.dhash(ob_img)
        self.whash = imagehash.whash(ob_img)
        self.file_size = os.path.getsize(imgpath)
