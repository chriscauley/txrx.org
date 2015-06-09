EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_USER = 'chris@lablackey.com'
EMAIL_HOST_USER = 'chris@lablackey.com'
EMAIL_HOST_PASSWORD = 'ee0ec710-7374-4a22-a726-703befff68f2'
EMAIL_PASSWORD = 'ee0ec710-7374-4a22-a726-703befff68f2'
EMAIL_SUBJECT_PREFIX = "[TXRX_DEV]"
DEFAULT_FROM_EMAIL = "noreply@txrxlabs.org"
PICS_EMAIL = 'txrxpics@gmail.com'
PICS_PASSWORD = 'everylittlethingshedoes'

DEBUG = True
LESS_EXECUTABLE = '/home/chriscauley/node/node_modules/less/bin/lessc'
SITE_URL = "http://durga.herefm.com:8009"
SITE_DOMAIN = "durga.herefm.com:8009"

# live site
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "616555778671-rv75tisfc5n3js62ac1j9lu55suko7l4.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "sQl0JmNX6kqAqexV4qCXWvnC"

# dev.txrxlabs.org
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "717494357012-5g8j9m9on5reg7m114fecmvsg4p1ml6h.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "QjHGLyt5FKufcijlolzWHnaE"

SOCIAL_AUTH_GITHUB_KEY = "a9d514aeddb8293b35b1"
SOCIAL_AUTH_GITHUB_SECRET = "e9ed7d10d3dd0d1856f2f79bf3601f58964e3b89"

SOCIAL_AUTH_FACEBOOK_KEY = ""
SOCIAL_AUTH_FACEBOOK_SECRET = ""

#THUMBNAIL_DUMMY = True
#THUMBNAIL_DEBUG = True
#THUMBNAIL_DUMMY_SOURCE = 'http://placekitten.com/%(width)s/%(height)s/'
THUMBNAIL_DUMMY_SOURCE = "placereddit"
THUMBNAIL_SUBREDDITS = ['aww','unlikelyfriends','turtles','cats','dogs']
THUMBNAIL_DUMMY_RATIO = "1.5"
PAYPAL_RECEIVER_EMAIL = "txrxlabs@gmail.com"
LONG_CACHE = 0

GOOGLE_CALENDAR_APY_KEY = "9-axWQ1FtYIFMKcfJZy9awyD"

from __init__ import SPATH
import os

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'txrx',
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'HOST': '',
    'PORT': '',
  },
  'anon': { #db for sharing stuff with the developers
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(SPATH,'../scripts/anon.db'),
  }
}

aDATABASES = {
  'default': { #db for sharing stuff with the developers
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(SPATH,'../scripts/anon.db'),
  }
}


COMPRESS_ENABLED = False

RECAPTCHA_PUBLIC_KEY = '6Lc53egSAAAAAFuu4PgoRVw_2ONjTTCfwkfDCFxF'
RECAPTCHA_PRIVATE_KEY = '6Lc53egSAAAAACCvXuucwYu_M3mn-ZQsOlc4Ly_0'
ALLOWED_EMAILS = ['chris@lablackey.com','cauley.chris@gmail.com','felixc@6ft.com']

TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
)

FAVICON = '/static/devicon.png'

PORTAL_KEY = '2Yiax9lNuiLuUZ6ZhZD38ZwQGud5J2RQlXoNsqqltsgrioFGq7'
