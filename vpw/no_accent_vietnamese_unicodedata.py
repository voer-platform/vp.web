#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Chương trình chuyển đổi từ Tiếng Việt có dấu sang Tiếng Việt không dấu
"""

import re
import unicodedata


def no_accent_vietnamese(s):
    try:
        s = s.decode('utf-8')
    except UnicodeEncodeError:
        # it seems input string is utf-8 ready
        pass
    s = re.sub(u'Đ', 'D', s)
    s = re.sub(u'đ', 'd', s)
    s = re.sub(u' ', '_', s)
    return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')

if __name__ == '__main__':
    print no_accent_vietnamese("Việt Nam Đất Nước Con Người")
    print no_accent_vietnamese("Welcome to Vietnam !")
    print no_accent_vietnamese("VIỆT NAM ĐẤT NƯỚC CON NGƯỜI")
