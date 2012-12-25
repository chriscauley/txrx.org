INSTALLED_APPS = (
  'grappelli',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.markup',
  'django.contrib.messages',
  'django.contrib.comments',
  'django.contrib.staticfiles',
  'django.contrib.humanize',
  'django.contrib.flatpages',
  'django.contrib.admin',
  #'template_utils',

  # 3rd party
  'south',
  'devserver',
  'sorl.thumbnail',
  'registration',
  'paypal.standard.ipn',
  'password_reset',
  'compressor',
  'tagging',

  # comments
  'mptt',
  'mptt_comments',

  # blarg
  'wmd',
  'password_reset',
  'codrspace',
  'tastypie',

  # lablackey
  'lablackey.photo',
  'lablackey.geo',
  'lablackey.profile',
  #'lablackey.djangogcal',
  'lablackey.db',

  # this project
  #'project',
  #'tool',
  'course',
  'membership',
  'main',
  'event',
)

#mptt_comments
COMMENTS_APP = 'mptt_comments'

LOGOUT_REDIRECT = 'home'

#compress
COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (('text/less', 'lessc {infile} {outfile}'),)

#codrspace
SITE_TAGLINE = "Houston's Hackerspace"
VERSION = "0.1 Alpha"
ANALYTICS_CODE = ''

from frappy.services.github import Github

# Information for correct authentication with github
# Replace with information specific to your app, etc.
GITHUB_AUTH = {
  'client_id': '',
  'secret': '',
  'callback_url': 'http://txrx.lablackey.com:8009/blog/signin_callback',
  'auth_url': 'https://github.com/login/oauth/authorize',
  'access_token_url': 'https://github.com/login/oauth/access_token',
  
  # Get information of authenticated user
  'user_url': 'https://api.github.com/user',
  
  # Debug mode - for faking auth_url
  'debug': False
  }

# set this to the JSON that comes back from http://api.github.com/user/
#user = Github().users(GITHUB_AUTH['username'])
#GITHUB_USER_JSON = user.response_json
