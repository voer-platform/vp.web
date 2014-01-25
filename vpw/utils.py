#!/usr/bin/env python
# -*- coding: utf-8 -*-

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