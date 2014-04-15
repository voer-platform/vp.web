#!/usr/bin/env python
# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import formatter

from django.utils.safestring import mark_safe
import re
import unicodedata


def normalize_string(value):
    """
    Converts to lowercase, removes non-word characters but still keep alphanumerics
    and converts spaces to hyphens. Also strips leading and trailing whitespace.
    Also converts vietnamese characters 'Đ' and 'đ'.
    """
    value = re.sub(u'Đ', 'D', value)
    value = re.sub(u'đ', 'd', value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\d\s-]', '', value).strip().lower()
    return mark_safe(re.sub('[-\s]+', '-', value))


def normalize_filename(value):
    value = re.sub(u'Đ', 'D', value)
    value = re.sub(u'đ', 'd', value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\.\w\d\s-]', '', value).strip().lower()
    return mark_safe(re.sub('[-\s]+', '-', value))


class ImageParse(HTMLParser):
    def __init__(self):        # class constructor
        HTMLParser.__init__(self)  # base class constructor
        self.url_images = []        # create an empty list for storing images

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.url_images.append(dict(attrs)["src"])

    def get_images(self):     # return the list of extracted images
        return self.url_images


def extract_images(content):
    image_parse = ImageParse()
    image_parse.feed(content)
    return image_parse.url_images
