'''
@author: nampnq
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
        'USER': 'travis',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}

#VPR Address
VPR_URL = 'http://dev.voer.vn:2013/1.0/'

#VPT Address
VPT_URL = 'http://dev.voer.vn:6543/'

SITE_URL = 'dev.voer.vn'

RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

#STATIC_ROOT = os.path.join(PROJECT_DIR, '_static')


COMPRESS_ENABLED = False
