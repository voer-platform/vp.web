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

LOGIN_URL = '/user/login/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p-z#m!yb%6(3k6fq+=mq6ikr@bbcjlp-gn8mu)ec#6x86tz+*7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['localhost', 'dev.voer.vn', 'voer.edu.vn']


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'registration',
    'tinymce',
    'sorl.thumbnail',
    'mce_filebrowser',
    'south',
    'vpw',
    'gunicorn',
    'compressor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'voer.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

LANGUAGES = (
    ('en', 'English'),
    ('vi', 'Vietinamese')
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = 'voer.urls'

WSGI_APPLICATION = 'voer.wsgi.application'

SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
)

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
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs/errors.log'),
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}


## REGISTER
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
EMAIL_HOST=''
EMAIL_PORT=25
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ''
VOER_FACEBOOK_APP_ID = ''
## END REGISTER
#
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static'),
)

VPR_URL = '' # URL VPR
VPR_PORT = '' # PORT VPR
VPR_VERSION = '' # VPR Version
VPR_URL_FULL = os.path.join(VPR_URL, VPR_PORT, VPR_VERSION)

CLIENT_ID = 'vpw'
CLIENT_KEY = ''

VPW_SESSION_MAX_AGE = 1 # days

SITE_URL = 'voer.edu.vn' # URL Site

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'

TINYMCE_JS_URL = MEDIA_URL + "tiny_mce/tiny_mce.js"
TINYMCE_JS_ROOT = os.path.join(MEDIA_ROOT, "tiny_mce")

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'skin': "cirkuit",
    'plugins': "autolink,lists,spellchecker,style,layer,table,advhr,advlink,emotions,iespell,latex,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras",
    'theme_advanced_buttons1': "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,formatselect,fontsizeselect,|,code,fullscreen,preview",
    'theme_advanced_buttons2': "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,|,forecolor,backcolor",
    'theme_advanced_buttons3': "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,latex,media",
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'theme_advanced_statusbar_location': "bottom",
    'theme_advanced_resizing': True,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'extended_valid_elements': 'figure,figcaption,maction,maligngroup,malignmark,math,menclose,merror,mfenced,mfrac,mglyph,mi,mlabeledtr,mlongdiv,mmultiscripts,mn,mo,mover,mpadded,mphantom,mroot,mrow,ms,mscarries,mscarry,msgroup,msline,mspace,msqrt,msrow,mstack,mstyle,msubsup,msup,mtable,mtd,mtext,mtr,munder,munderover,semantics,sub,mfrac,sup,annotation',
    'file_browser_callback': 'mce_filebrowser',
    'width': '730',
    'height': '400',
    'convert_urls': False
}


# COMPRESSOR

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "20971520"

GOOGLE_ANALYTICS_ID = ""
