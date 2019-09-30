#!/usr/bin/env python
# coding=utf-8
"""
use encoding utf-8
"""

import hashlib
import hmac
import json

import requests


def create_sha256_signature(secret, message):
    """
    Args:
        secret - required
        message - requred
    """
    secret = str(secret)
    message = str(message)
    secret_byte = str(secret).encode('utf-8')
    message_byte = str(message).encode('utf-8')
    signature = hmac.new(secret_byte, message_byte, hashlib.sha256).hexdigest()
    return signature


def sorted_tostring(unsorted_dict):
    """
    Args:
        unsorted_dict - required
    """
    new_string = ''
    for key, value in sorted(unsorted_dict.items()):
        new_string = new_string + str(key) + str(value)
    return new_string


class Client(object):
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

    def upload(self, api_secret=None, digital_content=None):
        """
        Upload digital conent to server
        """
        sorted_meta_media = sorted_tostring(digital_content.meta_media)
        signature = create_sha256_signature(str(api_secret),
                                            str(sorted_meta_media))
        #  print(signature)
        #  print(sorted_meta_media)
        #  print(type(sorted_meta_media))
        if self.host_url is None or self.api_key is None:
            raise Exception("Require host_url and api_key")

        headers = {
            "x-api-key": self.api_key,
            "x-api-sign": signature,
            'content-type': 'application/json'
        }
        if len(digital_content.meta_media) == 0:
            raise Exception("Meta Media does not set")

        response = requests.post(
            (self.host_url + "/checker"),
            json={
                "digest": digital_content.digest,
                "sha256": digital_content.sha256,
                "size_file": digital_content.file_size,
                "meta_media": digital_content.meta_media,
                "type": digital_content.type
            },
            headers=headers)
        print("content:" + str(response.text))
        return json.loads(response.text)
