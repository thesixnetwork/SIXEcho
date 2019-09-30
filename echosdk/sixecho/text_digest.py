#!/usr/bin/env python
# coding=utf-8
"""
use encoding utf-8
"""
from __future__ import print_function

import base64
import binascii
import concurrent
import hashlib
import hmac
import json
import os
from concurrent.futures import ThreadPoolExecutor

import epub_conversion as ec
import imagehash
import PyPDF2
import requests
from datasketch import MinHash
from epub_conversion.utils import open_book
from PIL import Image
from pythainlp import word_tokenize

from .echo_util import print_progress_bar

#  def mygrouper(n, iterable):
#  """
#  mygrouper is group
#  Args:
#  n - Required : number
#  iterable - Required :
#  """
#  args = [iter(iterable)] * n
#  return ([e for e in t if e != None] for t in itertools.zip_longest(*args))


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
    words = word_tokenize(str, engine="dict")
    new_words = [word for word in words if word != ' ']
    return new_words


def tokenize_mutiline(lines=[]):
    """
    Tokenzie mutiline
    Args:
        lines - Required : array of sentances
    Returns:
        Arrays words
    """
    result = []
    if len(lines) == 0:
        return result
    with ThreadPoolExecutor(max_workers=len(lines)) as executor:
        future_to_url = {
            executor.submit(tokenize, line): line
            for line in lines
        }
        for future in concurrent.futures.as_completed(future_to_url):
            data = future.result()
            result = result + data
        return result


class Text(object):
    """
    client class to control api with restful
    """
    def __init__(self, api_key=None, host_url=None):
        """
        Initial sixecho
        Attributes:
            api_key(string)       - Optional : api_key generate from sixecho
            host_url(string)      - Optional : is sixecho domain
        """
        self.api_key = api_key
        if host_url is not None:
            if host_url.endswith("/"):
                host_url = host_url[:-1]
            self.host_url = host_url
        self.array_words = []
        self.min_hash = MinHash(num_perm=128)
        self.max_workers = 1
        self.sha256 = ""
        self.file_size = 0
        self.meta_media = None
        self.type = "TEXT"
        self.digest = ""

    #  def digest(self):
    #  """Export the hash values, which is the internal state of the
    #  MinHash.

    #  Returns:
    #  numpy.array: The hash values which is a Numpy array.
    #  """
    #  return self.min_hash.digest()

    def generate(self, str=None, txtpath=None, epubpath=None, pdfpath=None):
        """Generate minhash with new value from string or file
        we use minhash from https://ekzhu.github.io/datasketch/_modules/datasketch/minhash.html#MinHash.update
        Args:
            str(string)     - Optional  :   string whose minhash to be computed.
            txtpath(string)   - Optional  :   path of text file to be computed.
            epubpath(string)   - Optional  :   path of epub file to be computed.
            pdfpath(string)   - Optional  :   path of pdf file to be computed.
        """
        if txtpath:
            self.load_file(txtpath)
        elif epubpath:
            size = len(epubpath.split('.'))
            name = epubpath.split('.')[size - 2]
            size = len(name.split('/'))
            name = name.split('/')[size - 1]
            name = name.replace("/", "")
            name = name + '.txt'
            cur_path = os.path.dirname(os.path.abspath(__file__))
            self.write2text(self.readepub(epubpath), name)
            self.load_file(cur_path + '/' + name)
            os.remove(cur_path + '/' + name)
        elif pdfpath:
            size = len(pdfpath.split('.'))
            name = pdfpath.split('.')[size - 2]
            size = len(name.split('/'))
            name = name.split('/')[size - 1]
            name = name.replace("/", "")
            name = name + '.txt'
            cur_path = os.path.dirname(os.path.abspath(__file__))
            self.write2text(self.readpdf(pdfpath), name)
            self.load_file(cur_path + '/' + name)
            os.remove(cur_path + '/' + name)

        else:
            sha256 = hashlib.sha256()
            sha256.update(str.encode())
            self.sha256 = sha256.hexdigest()
            self.array_words = tokenize(str)
            self.file_size = len(str)
            for d in self.array_words:
                self.min_hash.update(d.encode('utf8'))
        self.make_digest()

    def set_meta(self, meta_books):
        """
        Args:
            meta_books(Hash)      - Require  : struct books include
                - category_id(string) - Require : category of books you can get from search category api
                - publisher_id(string) - Require : publisher of book you can get from search publisher api
                - title(string) - Require : title book
                - auther(string) - Require : auther book
                - country_of_origin(string) : country iso 3166-1
                - language(string) Require : language iso 639-1
                - paperback(string) Require : total page book
                - publish_date(string) Require : publish date
        """
        self.meta_media = meta_books

    def create_sha256_signature(self, secret, message):
        secret = str(secret)
        message = str(message)
        # print(secret, message)
        # print(type(secret))
        # print(type(message))
        secret_byte = str(secret).encode('utf-8')
        message_byte = str(message).encode('utf-8')
        signature = hmac.new(secret_byte, message_byte,
                             hashlib.sha256).hexdigest()
        return signature

    def make_digest(self):
        self.digest = ",".join([str(num) for num in self.min_hash.digest()])

    def load_file(self, fpath):
        """
        method load_file
        """
        sha256 = hashlib.sha256()
        f_count = open(fpath, "r")
        f = f_count.readlines()
        f_count.close()
        list_of_groups = None
        if self.max_workers != 1:
            l = f
            n = self.max_workers
            list_of_groups = [l[i:i + n] for i in range(0, len(l), n)]
            #  list_of_groups = zip(*(iter(f), ) * self.max_workers)

        file_size = os.path.getsize(fpath)
        print_progress_bar(0,
                           file_size,
                           prefix='Progress:',
                           suffix='Complete',
                           length=50)
        progress = 0
        lines = []
        if self.max_workers == 1:
            for line in f:
                progress = progress + len(line)
                sha256.update(line.encode())
                words = tokenize(line)
                if len(words) != 0:
                    for d in words:
                        self.min_hash.update(d.encode('utf8'))
                print_progress_bar(progress,
                                   file_size,
                                   prefix='Progress:',
                                   suffix='Complete',
                                   length=50)
        else:
            for line in f:
                sha256.update(line.encode())
            for lines in list_of_groups:
                for line in lines:
                    progress = progress + len(line)
                words = tokenize_mutiline(lines)
                if len(words) != 0:
                    for d in words:
                        self.min_hash.update(d.encode('utf8'))
                print_progress_bar(progress,
                                   file_size,
                                   prefix='Progress:',
                                   suffix='Complete',
                                   length=50)
        self.sha256 = sha256.hexdigest()
        self.file_size = file_size

    def readepub(self, fpath):
        list_text = []
        book = open_book(fpath)
        lines = ec.utils.convert_epub_to_lines(book)
        for line in lines:

            text = ec.utils.convert_lines_to_text(str(line), "txt")
            text = list(text)
            for ele in text:
                list_text.append(ele)
        return list_text

    def readpdf(self, fpath):
        pdfFileObj = open(fpath, 'rb')  # 'rb' for read binary mode
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        total_page = pdfReader.numPages
        # print(total_page)
        list_text = []
        for i in range(total_page):
            pageObj = pdfReader.getPage(i)
            list_text.append(pageObj.extractText())
        return list_text

    def write2text(self, list_text, opname):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        fpath = opname
        print(cur_path)
        print(cur_path + '/' + fpath)
        file = open(cur_path + '/' + fpath, 'w')
        for ele in list_text:
            file.write(ele)
        file.close()
