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
PROJECT_DIR = os.path.join(SETTING_DIR, '../')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p-z#m!yb%6(3k6fq+=mq6ikr@bbcjlp-gn8mu)ec#6x86tz+*7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

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
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
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

ROOT_URLCONF = 'voer.urls'

WSGI_APPLICATION = 'voer.wsgi.application'


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

VPR_URL = 'dev.voer.vn'
VPR_PORT = '2013'
VPR_VERSION = '1.0'
VPR_URL_FULL = os.path.join(VPR_URL, VPR_PORT, VPR_VERSION)

SITE_URL = 'voer.edu.vn'
