'''
Created on 16 Dec 2013

@author: huyvq
'''
from base import *

# FOR DEBUG
DEBUG = True
DEVELOPMENT = True
TEMPLATE_DEBUG = DEBUG

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'voer_django',
        'USER': 'voer',
        'PASSWORD': 'voer',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}

#VPR Address
VPR_URL = 'http://dev.voer.vn:2013/1.0/'

#VPT Address
VPT_URL = 'http://voer.edu.vn:6543/'

SITE_URL = 'dev.voer.vn'

