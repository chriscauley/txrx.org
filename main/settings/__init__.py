import os, sys, datetime
SPATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0,os.path.normpath(os.path.join(SPATH,'../.dev/')))
sys.path.insert(0,os.path.normpath(SPATH))
sys.path.insert(0,os.path.normpath(os.path.join(SPATH,'..'))) # this is to use txrx.org/media not .dev/media

DEBUG = True

MANAGERS = ADMINS = (
  ('chris cauley','chris@lablackey.com'),
)

INTERNAL_IPS = (
  '50.194.167.97', #TXRX
)

DJSTRIPE_CUSTOMER_REQUIRED = False
DROP_PAYMENT_BACKENDS = [
  'drop.payment.backends.stripe_backend.Stripe',
  'drop.giftcard.backend.GiftCard',
]
DROP_CART_MODIFIERS = [
  'drop.cart.modifiers.partial_payment.PartialPaymentModifier',
  'drop.discount.modifier.UserDiscountCartModifier',
]
DROP_GET_OR_CREATE_CUSTOMER = 'course.utils.get_or_create_student'
DROP_GIFTCARD_LANDING = "/classes/"
DROP_GIFTCARD_IMG = os.path.join(SPATH,"static/img/giftcard_base.png")
DROP_GIFTCARD_FONT = os.path.join(SPATH,"static/fonts/roboto/Roboto-Regular.ttf")
DROP_USER_DISCOUNT_ITEM_FUNCTION = "user.models.get_item_discount"
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

DEVSERVER_DEFAULT_ADDR = "0.0.0.0"
DEVSERVER_DEFAULT_PORT = 8025

# Site specific settings for handling membership
ALL_HOURS_ID = 2 # which schedule is 24/7?
REQUIRED_DOCUMENT_IDS = [1,2,3]
NONMEMBER_DOCUMENT_IDS = [2]
ORIENTATION_EVENT_ID = 105
DEFAULT_MEMBERSHIP_LEVEL = 1
PAST_DUE_GRACE_PERIOD = 14 # Past due members will get kicked out of their drawer after this many days

ALLOWED_HOSTS = ['.txrxlabs.org']

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(SPATH, '../.media')
MEDIA_URL = '/media/'
UPLOAD_DIR = 'uploads'
STATIC_ROOT = os.path.join(SPATH,'../.static')
STATIC_URL = '/static/'
STAFF_ROOT = os.path.join(SPATH, '../.staff')
STAFF_URL = '/staff_only/'
PRIVATE_ROOT = os.path.normpath(os.path.join(SPATH, '../.private'))

LOGIN_URL = "/accounts/login/"
LOGOUT_URL = "/accounts/logout/"
LOGIN_REDIRECT_URL = "/"

SECRET_KEY = '^f_fn6)^e5^)+p-rjcrcdf(7iwz4@5z9thx92%^=e_)$jly7mc'
MAPS_API_KEY = 'ABQIAAAAeppD1h9lB7H61ozR18SeZRS_YqHDtehKcRTrrAGjc25rDMjatxT8nvoX4-jJXcRPaT4I-RdMYv3fJA'
TEST_RUNNER = 'main.runner.Runner'

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTH_USER_MODEL = 'user.User'
REGISTRATION_IGNORE_DOTS = True

AUTHENTICATION_BACKENDS = (
  #'social.backends.open_id.OpenIdAuth',
  #'social.backends.google.GoogleOpenId',
  'social.backends.google.GoogleOAuth2',
  'social.backends.facebook.FacebookOAuth2',
  'social.backends.github.GithubOAuth2',
  #'social.backends.google.GoogleOAuth',
  #'social.backends.twitter.TwitterOAuth',
  #'social.backends.yahoo.YahooOpenId',
  'main.backends.EmailOrUsernameModelBackend',
  'django.contrib.auth.backends.ModelBackend'
)

PIPELINE = (
  'social.pipeline.social_auth.social_details',
  'social.pipeline.social_auth.social_uid',
  'social.pipeline.social_auth.auth_allowed',
  'social.pipeline.social_auth.social_user',
  'social.pipeline.user.get_username',
  # 'social.pipeline.mail.mail_validation',
  'social.pipeline.social_auth.associate_by_email',
  'social.pipeline.user.create_user',
  'social.pipeline.social_auth.associate_user',
  'social.pipeline.social_auth.load_extra_data',
  'social.pipeline.user.user_details'
)

REST_FRAMEWORK = {
  'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticated',
  ),
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
  ),
}

ROOT_URLCONF = 'main.urls'

from django.contrib import messages
MESSAGE_TAGS = { messages.ERROR: 'danger' }

STATICFILES_DIRS = (os.path.join(SPATH,"static"),)

STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  # other finders..
  'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
  ('text/less', 'lessc {infile} {outfile}'),
  ('riot/tag', 'riot {infile} {outfile}'),
)

ACCOUNT_ACTIVATION_DAYS = 7

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SITE_URL = "https://txrxlabs.org"
SITE_DOMAIN = "txrxlabs.org"
SITE_NAME = "TXRX Labs"
WEBMASTER = "chris@lablackey.com"

PUBLIC_SETTINGS = ["DEBUG","SITE_NAME","SITE_DOMAIN","SITE_URL"]

LONG_CACHE = 60*60 # 1h
SHORT_CACHE = 10*60 # 10 min

PAYPAL_RECEIVER_EMAIL = "txrxlabs@gmail.com"

CONTACT_EMAIL = "webmaster@txrxlabs.org"
CONTACT_LINK = "<a href='%s'>%s</a>"%(CONTACT_EMAIL,CONTACT_EMAIL)
EMAIL_SUBJECT_PREFIX = "[TXRX] "
DEFAULT_FROM_EMAIL = "noreply@txrxlabs.org"
SERVER_EMAIL = "noreply@txrxlabs.org"
MEMBERSHIP_EMAIL = "info@txrxlabs.org"
PURCHASING_EMAIL = "membership@txrxlabs.org"

PER_PAGE = 10
NEW_STUDENT_PASSWORD = "I am a new student, reset my passwrod asap"

for s_file in ['apps','local','txrx_labs']:
  try:
    f = 'main/settings/%s.py'%s_file
    exec(compile(open(os.path.abspath(f)).read(), f, 'exec'), globals(), locals())
  except IOError:
    print "Setting file missing. We looked here: %s"%f



EMAIL_BACKEND = "mailer.backend.DbBackend"
_TEMPLATE_LOADERS = (
  ('django.template.loaders.cached.Loader', (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'lablackey.tloader.Loader',
  )),
)

if DEBUG:
  EMAIL_BACKEND = "lablackey.mail.DebugBackend"
  _TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'lablackey.tloader.Loader',
  )

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
      os.path.join(SPATH,"templates"),
      os.path.join(SPATH,"../lablackey/templates"),
    ],
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.template.context_processors.media',
        'django.template.context_processors.static',
        "django.core.context_processors.i18n",
        'django.contrib.auth.context_processors.auth',
        'django.template.context_processors.request',
        'django.template.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'social.apps.django_app.context_processors.backends',
        'social.apps.django_app.context_processors.login_redirect',
        'main.context.nav',
        'main.context.motd',
        'blog.context.process',
      ],
      'loaders': _TEMPLATE_LOADERS
    },
  },
]

DEFAULT_PHOTO_ID = 144
