INSTALLED_APPS = (
  'lablackey',
  'suit',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.sitemaps',
  'django.contrib.messages',
  'django_comments',
  'django.contrib.staticfiles',
  'django.contrib.humanize',
  'django.contrib.flatpages',
  'django.contrib.admin',
  #'template_utils',

  # 3rd party
  #'markdown_deux',
  #'bootstrapform',
  'sorl.thumbnail',
  'registration',
  'paypal.standard.ipn',
  'compressor',
  'tagging',
  'crop_override',
  'social.apps.django_app.default',
  'rest_framework',
  'jsignature',

  #store
  'shop',
  'store',

  # comments
  'mptt',
  'mptt_comments',

  # blarg
  'wmd',
  'blog',
  'media',

  # this project
  'user',
  'geo',
  'misc',
  #'project',
  'instagram',
  'tool',
  'contact',
  'course',
  'membership',
  'main',
  'event',
  'thing',
  'notify',
  'api',
  'redtape',
  'schedule_poll',
)

#mptt_comments
COMMENTS_APP = 'mptt_comments'
MPTT_COMMENTS_CUTOFF = 0

LOGOUT_REDIRECT = 'home'

#compress
COMPRESS_ENABLED = True

#codrspace
SITE_TAGLINE = "Houston's Hackerspace"
VERSION = "0.1 Alpha"
ANALYTICS_CODE = ''

INSTAGRAM_TAG = "txrx"
INSTAGRAM_EMAIL = ['chris@lablackey.com']
INSTAGRAM_TOKEN = "3794301.f59def8.e08bcd8b10614074882b2d1b787e2b6f"

THUMBNAIL_DUMMY = True
THUMBNAIL_DEBUG = True
THUMBNAIL_DUMMY_SOURCE = "placereddit"
THUMBNAIL_DUMMY_RATIO = "1.5"

RECAPTCHA_PUBLIC_KEY = '6Lc53egSAAAAAFuu4PgoRVw_2ONjTTCfwkfDCFxF'
RECAPTCHA_PRIVATE_KEY = '6Lc53egSAAAAACCvXuucwYu_M3mn-ZQsOlc4Ly_0'

# Django Suit configuration example
SUIT_CONFIG = {
  # header
  'ADMIN_NAME': 'TXRX Labs',
  'SEARCH_URL': '/admin/user/user/',
  # 'HEADER_DATE_FORMAT': 'l, j. F Y',
  # 'HEADER_TIME_FORMAT': 'H:i',

  # forms
  # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
  # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

  # menu
  # 'MENU_ICONS': {
  #  'sites': 'icon-leaf',
  #  'auth': 'icon-lock',
  # },
  # 'MENU_OPEN_FIRST_CHILD': True, # Default True
  # 'MENU_EXCLUDE': ('auth.group',),
  'MENU': (
    'blog',
    'contact',
    {'app': 'course',
     'icon':'icon-calendar',
     'models': (
       #'course.branding', #accessible thorugh course.course
       'course.course',
       'course.enrollment',
       'course.evaluation',
       'geo.location',
       'geo.room',
       'course.session',
       'course.subject',
       #'course.term', #accessible through course.session
     )
    },
    #'default', # social-auth
    {'app': 'event',
     'icon':'icon-calendar',
     'models': (
       'event.event',
       'event.eventoccurrence',
       'geo.location',
       'geo.room',
     )
    },
    #'feed', # not implimented
    #'geo', #occurs in several other places
    #'ipn', #paypal ipns
    {'app': 'media',
     'models': (
       {'model': 'mptt_comments.mpttcomment', 'label':'Comments'},
       'flatpages.flatpage',
       'media.miscfile',
       'media.photo',
       'media.phototag',
     )
    },
    {'app': 'membership',
     'icon':'icon-user',
     'models': (
       'membership.meetingminutes',
       'membership.levels',
       'membership.group',
       'membership.officer',
       'membership.subscription',
       'membership.flag',
       'user.user',
     )
    },
    'mptt_comments'
    'notify',
    'registration',
    #'sites',
    #'tagging',
    'store',
    'thing',
    'tool',
    #{'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
    #{'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
  ),

  # misc
  'LIST_PER_PAGE': 200
}
"""
Instagram
Ipn
Media
Membership
Mptt_Comments
Notify
Registration
Sites
Tagging
Thing
Tool
"""
