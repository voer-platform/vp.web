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
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}

VPR_URL = 'dev.voer.vn'
VPR_PORT = '2013'
VPR_VERSION = '1.0'
VPR_URL_FULL = os.path.join(VPR_URL, VPR_PORT, VPR_VERSION)

SITE_URL = 'dev.voer.vn'

#VPR Address
VPR_URL = 'http://dev.voer.vn:2013/1.0/'

#VPT Address
VPT_URL = 'http://dev.voer.vn:6543/'
VOER_FACEBOOK_APP_ID = 473667049342331

RECAPTCHA_PUBLIC_KEY = '6Lf__uwSAAAAAPpTMYOLUOBf25clR7fGrqWrpOn0'
RECAPTCHA_PRIVATE_KEY = '6Lf__uwSAAAAAPlCihico8fKiAfV09_kbywiI-xx'


COMPRESS_ENABLED = False
THUMBNAIL_DEBUG = False
DEBUG = True
