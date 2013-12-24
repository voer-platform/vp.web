"""
Django settings for voer project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

SETTING_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.join(SETTING_DIR, '../../')

LOGIN_URL='/user/login/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p-z#m!yb%6(3k6fq+=mq6ikr@bbcjlp-gn8mu)ec#6x86tz+*7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'registration',
    'south',
    'vpw',
    'gunicorn',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

LANGUAGES=(
    ('en', 'English'),
    ('vi', 'Vietinamese')
)

ROOT_URLCONF = 'voer.urls'

WSGI_APPLICATION = 'voer.wsgi.application'




# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': [],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}


## REGISTER
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
EMAIL_HOST='email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT=25
EMAIL_HOST_USER='AKIAJYYWT53Z4KQZMHUA'
EMAIL_HOST_PASSWORD='AhM4gp8514eJB7Fv2kg4Z2Idj4kPEVXtHotO664Ggzc4'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'info@voer.edu.vn'
VOER_FACEBOOK_APP_ID = 271167089707244
## END REGISTER
#
STATICFILES_DIRS = [os.path.join(PROJECT_DIR, 'static')]

VPR_URL = '' # URL VPR
VPR_PORT = '' # PORT VPR
VPR_VERSION = '' # VPR Version
VPR_URL_FULL = os.path.join(VPR_URL, VPR_PORT, VPR_VERSION)

SITE_URL = 'voer.edu.vn' # URL Site
