from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm

from tagging.models import Tag

from event.models import EventOccurrence

import datetime

def nav(request):
  blog_sublinks = [
    {'name': 'Blog Home', 'url': '/blog/', 'pjax': True},
    {'name': 'Add Post', 'url': '/blog/admin/add/'},
    {'name': 'My Posts', 'url': '/blog/%s/'%request.user.username},
    ]
  _nav = [
    {"name": "Classes",
     "url": "/classes/",
     'sublinks': [
        {"name": "All classes", "url": "/classes/", 'pjax': True},
        {"name": "My classes", "url": "/classes/my-sessions/", 'pjax': True},
        ]
     },
    {"name": "Blog",
     "url": "/blog/",
     'pjax': True,
     "sublinks": blog_sublinks if request.user.is_staff else [],
     },
    {'name': "Join us", "url": "/join-us/", 'pjax': True},
    {'name': "Location", "url": "/map/", 'pjax': True},
    ]
  today = datetime.date.today()

  return dict(
    current = request.path.split('/')[1] or 'home',
    nav = _nav,
    STATIC_URL = settings.STATIC_URL,
    auth_form = AuthenticationForm,
    app_path = "/admin/login/",
    next = request.path,
    settings = settings,
    upcoming_events = EventOccurrence.objects.filter(start__gte=today)[:5],
    tags = Tag.objects.all(),
    )
