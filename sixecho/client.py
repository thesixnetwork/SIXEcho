#!/usr/bin/env python
# coding=utf-8
"""
"""
from __future__ import print_function
from datasketch import MinHash
import deepcut
import time
import os
import requests
import json
import hashlib


def tokenize(str):
    """
    Tokenize given Thai, English text string
    Args:
       str - Required : Thai, English, Mix(Thai,English) text string
    Returns:
       tokens: list, list of tokenized words
    Example
    >> sixecho.tokenize('I am a developer python newly. ผมเป็นมือใหม่สำหรับ python')
    >> ['I','am','a','developer','python','newly','.','ผม','เป็น','มือ','ใหม่','สำหรับ','python']
    """
    words = deepcut.tokenize(str)
    new_words = [word for word in words if word != ' ']
    return new_words


def printProgressBar(iteration, total, prefix='Progress', suffix='Complete', decimals=1, length=100, fill='='):
    """
    Call in a loop to create terminal progress bar
    Args:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end="\r")
    # Print New Line on Complete
    if iteration == total:
        print()


class Client(object):
    def __init__(self, api_key=None, host_url=None):
        """
        Initial sixecho
        Attributes:
            api_key(string)       - Optional : api_key generate from sixecho
            host_url(string)      - Optional : is sixecho domain
        """
        self.api_key = api_key
        if host_url != None:
            if host_url.endswith("/"):
                host_url = host_url[:-1]
            self.host_url = host_url
        self.array_words = []
        self.min_hash = MinHash(num_perm=128)

    def digest(self):
        """Export the hash values, which is the internal state of the
        MinHash.

        Returns:
            numpy.array: The hash values which is a Numpy array.
        """
        return self.min_hash.digest()

    def generate(self, str=None, fpath=None):
        """Generate minhash with new value from string or file
        we use minhash from https://ekzhu.github.io/datasketch/_modules/datasketch/minhash.html#MinHash.update
        Args:
            str(string)     - Optional  :   string whose minhash to be computed.
            fpath(string)   - Optional  :   path file to be computed.
        """
        if fpath:
            self.load_file(fpath)
        else:
            sha256 = hashlib.sha256()
            sha256.update(str)
            self.sha256 = sha256.hexdigest()
            self.array_words = tokenize(str)
            for d in self.array_words:
                self.min_hash.update(d.encode('utf8'))

    def upload(self):
        """Upload digital conent to server

        """
        digest = ",".join([`num` for num in self.digest()])
        if self.host_url == None or self.api_key == None:
            raise Exception("Require host_url and api_key")

        headers = {
            "x-api-key": self.api_key,
            'content-type': 'application/json'
        }
        response = requests.post(
            (self.host_url + "/checker"), json={"digest": digest, "sha256": self.sha256}, headers=headers)
        print("content:" + str(response.text))
        return json.loads(response.text)

    def load_file(self, fpath):
        sha256 = hashlib.sha256()
        f = open(fpath, "r")
        fileSize = os.path.getsize(fpath)
        printProgressBar(0, fileSize, prefix='Progress:',
                         suffix='Complete', length=50)
        progress = 0
        for line in f:
            progress = progress + len(line)
            sha256.update(line)
            words = tokenize(line)
            for d in words:
                self.min_hash.update(d.encode('utf8'))
            printProgressBar(progress, fileSize,
                             prefix='Progress:', suffix='Complete', length=50)
        f.close()
        self.sha256 = sha256.hexdigest()
