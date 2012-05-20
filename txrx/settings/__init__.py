import os, sys
SPATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0,os.path.normpath(os.path.join(SPATH,'..')))

DEBUG = True; TEMPLATE_DEBUG = DEBUG

MANAGERS = ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

""" # example of the live database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'txrx',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '',
        'PORT': '',
    }
}"""

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'txrx.db',
    }
  }

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(SPATH, '../media')
MEDIA_URL = '/media/'
UPLOAD_DIR = 'uploads'
STATIC_ROOT = os.path.join(SPATH,'../static')
STATIC_URL = '/static/'

LOGIN_URL = "/login"
LOGOUT_URL = "/logout"
ROOT_URL = "http://txrxlabs.org/"

SECRET_KEY = '^f_fn6)^e5^)+p-rjcrcdf(7iwz4@5z9thx92%^=e_)$jly7mc'
EZGAUTH_KEY = 'monkeybutlersleepsatmidnight@5z9thx92%^=e_)$jly7mc'
JANRAIN_RPX_API_KEY = 'd8811e4889d480b090343b70e374ebeb7be05339'
MAPS_API_KEY = 'ABQIAAAAeppD1h9lB7H61ozR18SeZRS_YqHDtehKcRTrrAGjc25rDMjatxT8nvoX4-jJXcRPaT4I-RdMYv3fJA'

TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.contrib.auth.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.request",
  "django.contrib.messages.context_processors.messages",
  'context.nav',
)

ROOT_URLCONF = 'txrx.urls'

TEMPLATE_DIRS = (
  os.path.join(SPATH,"templates"),
  os.path.join(SPATH,"../lablackey/templates"),
)

INSTALLED_APPS = (
  'grappelli',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.humanize',
  'django.contrib.admin',

  # 3rd party
  'south',
  'devserver',
  'articles',
  'sorl.thumbnail',

  # lablackey
  'lablackey.photo',
  'lablackey.content',
  'lablackey.geo',
  'lablackey.profile',
  #'lablackey.djangogcal',
  'lablackey.db',

  # this project
  'txrx.tool',
  'txrx.course',
  'txrx.project',
  'txrx.membership',
  'txrx.main',
  'lablackey.event',
  'txrx.chore',
)

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
    'mail_admins': {
      'level': 'ERROR',
      'class': 'django.utils.log.AdminEmailHandler'
      }
    },
  'loggers': {
    'django.request': {
      'handlers': ['mail_admins'],
      'level': 'ERROR',
      'propagate': True,
      },
    }
  }

import re
import socket
# Remove characters that are invalid for python modules.
machine = re.sub('[^A-z0-9._]', '_', socket.gethostname())

try:
  istr = 'settings.' + machine
  tmp = __import__(istr)
  mod = sys.modules[istr]
except ImportError:
  print "No %r module found for this machine." % istr
else:
  for setting in dir(mod):
    if setting == setting.upper():
      setattr(sys.modules[__name__], setting, getattr(mod, setting))

try:
  istr = 'settings.local'
  tmp = __import__(istr)
  mod = sys.modules[istr]
except ImportError:
  print "No local settings found for this machine."
else:
  for setting in dir(mod):
    if setting == setting.upper():
      setattr(sys.modules[__name__], setting, getattr(mod, setting))
