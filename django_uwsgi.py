import os
import django.core.handlers.wsgi

os.environ['PYTHON_EGG_CACHE'] = '/tmp/egg_cache'
os.environ['DJANGO_SETTINGS_MODULE'] = 'txrx.settings'
application = django.core.handlers.wsgi.WSGIHandler()
