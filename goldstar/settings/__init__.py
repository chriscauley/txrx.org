import os, sys

SFILE = __file__
SPATH = os.path.normpath(os.path.join(os.path.dirname(SFILE), '..'))

dpath = os.path.normpath(os.path.join(SPATH, 'depends'))
if dpath not in sys.path:
  sys.path.insert(0, dpath)

LESS_EXECUTABLE = os.path.join(SPATH,"lessc")

MEDIA_ROOT = os.path.join(SPATH, 'media')
MEDIA_URL = '/site_media/media/'
STATIC_URL = '/site_media/static/'
STATIC_ROOT = os.path.join(SPATH,'main/static')
UPLOAD_DIR = 'uploads'
THUMBNAIL_FORMAT = "PNG"

# JanRain - linked to chriscauley@mouthwateringmedia.com
DEBUG = False
TEMPLATE_DEBUG = DEBUG

#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
VISITOR_ID_COOKIE_NAME = 'visitor_id'

ADMINS = (
    ('Chris', 'chris@lablackey.com'),
)

MANAGERS = ADMINS

SITE_NAME = 'TXRX gold star board'
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(SPATH, '../txrx.db')
    }
  }

AUTHENTICATION_BACKENDS = (
  'django.contrib.auth.backends.ModelBackend',
  )

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j+c#h$vnogpq3vb)v6l$d9aa5z4*$-)0a)z(7zh3=7ecb1_0z@'

STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  'compressor.finders.CompressorFinder',
  #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
  #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'goldstar.urls'

TEMPLATE_DIRS = (
  os.path.join(SPATH, 'templates'),
)

INSTALLED_APPS = (
  'grappelli',
  #'main',
  'django.contrib.admin',
  'django.contrib.admindocs',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.gis',
  'django.contrib.humanize',
  'django.contrib.markup',
  'django.contrib.messages',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.syndication',
  'django.contrib.staticfiles',
  #'photo',
  #'articles',
  #'event',
  'ajax_select',
  'compressor',
  'sorl.thumbnail',
  'south',
  'chores',
  #'cms',
  #'content',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.contrib.auth.context_processors.auth",
  "django.core.context_processors.request",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.request",
  "django.contrib.messages.context_processors.messages",
  "context.process",
)

GRAPPELLI_ADMIN_HEADLINE = 'TXRX Chores Administration'
GRAPPELLI_ADMIN_TITLE = 'TXRX Chores Administration'

# For ajax_select.
AJAX_LOOKUP_CHANNELS = {
  #'photo': ('photo.ajax_lookup', 'PhotoLookup'),
  }
AJAX_SELECT_BOOTSTRAP = True
AJAX_SELECT_INLINES = 'inline'
"""
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com.'
EMAIL_HOST_USER = 'logs@mouthwateringmedia.com'
EMAIL_HOST_PASSWORD = 'sX8TkXkb'
EMAIL_PORT = 587"""

import re
import socket
# Remove characters that are invalid for python modules.
machine = re.sub('[^A-z0-9._]', '_', socket.gethostname())

try:
  istr = 'settings.' + machine
  tmp = __import__(istr)
  mod = sys.modules[istr]
except ImportError:
  print "No %r module found for this machine" % istr
else:
  for setting in dir(mod):
    if setting == setting.upper():
      setattr(sys.modules[__name__], setting, getattr(mod, setting))

try:
    from local_settings import *
except ImportError:
    pass

ADMIN_MEDIA_PREFIX = "/site_media/static/gmedia/"
