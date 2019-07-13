'''
Created on 16 Dec 2013

@author: huyvq
'''
from base import *

# FOR DEBUG
DEBUG = DEVELOPMENT = TEMPLATE_DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vpw',
        'USER': 'voer',
        'PASSWORD': 'voer',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}

#VPR Address
VPR_URL = 'https://dev.voer.edu.vn:1122/1.0/'

#VPT Address
VPT_URL = 'https://dev.voer.edu.vn:1133/'

SITE_URL = 'dev.voer.edu.vn'
