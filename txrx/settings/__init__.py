import os, sys
SPATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0,os.path.normpath(SPATH))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MANAGERS = ADMINS = (
  ('chris cauley','chris@lablackey.com'),
)

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(SPATH,'txrx.db'),
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
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

LOGIN_URL = "/accounts/login/"
LOGOUT_URL = "/accounts/logout/"

SECRET_KEY = '^f_fn6)^e5^)+p-rjcrcdf(7iwz4@5z9thx92%^=e_)$jly7mc'
MAPS_API_KEY = 'ABQIAAAAeppD1h9lB7H61ozR18SeZRS_YqHDtehKcRTrrAGjc25rDMjatxT8nvoX4-jJXcRPaT4I-RdMYv3fJA'

TEMPLATE_LOADERS = (
    #('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    #)),
)

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'theme.middleware.Theme',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.contrib.auth.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.static",
  "django.core.context_processors.request",
  "django.contrib.messages.context_processors.messages",
  'txrx.context.nav',
  'txrx.context.motd',
  'txrx.context.evaluations',
  'codrspace.context_processors.codrspace_contexts',
)

ROOT_URLCONF = 'txrx.urls'

TEMPLATE_DIRS = (
  os.path.join(SPATH,"templates"),
  os.path.join(SPATH,"../lablackey/templates"),
)

STATICFILES_DIRS = (os.path.join(SPATH,"static"),)

STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  # other finders..
  'compressor.finders.CompressorFinder',
  )

ACCOUNT_ACTIVATION_DAYS = 7

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SITE_URL = "http://txrxlabs.org"
SITE_DOMAIN = "txrxlabs.org"
SITE_NAME = "TX/RX Labs"
WEBMASTER = "chris@lablackey.com"

LONG_CACHE = 60*60 # 1h
SHORT_CACHE = 10*60 # 10 min

AUTH_PROFILE_MODULE = 'codrspace.Profile'

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


PAYPAL_RECEIVER_EMAIL = "txrxlabs@gmail.com"

import re
import socket
# Remove characters that are invalid for python modules.
machine = re.sub('[^A-z0-9._]', '_', socket.gethostname())

EMAIL_SUBJECT_PREFIX = "[TXRX] "
DEFAULT_FROM_EMAIL = "noreply@txrxlabs.org"
SERVER_EMAIL = "noreply@txrxlabs.org"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

NEW_STUDENT_PASSWORD = "I am a new student, reset my passwrod asap"

for s_file in ['apps','local']:
  try:
    istr = 'txrx.settings.' + s_file
    tmp = __import__(istr)
    mod = sys.modules[istr]
  except ImportError:
    print "No %r module found for this machine." % istr
  else:
    for setting in dir(mod):
      if setting == setting.upper():
        setattr(sys.modules[__name__], setting, getattr(mod, setting))

