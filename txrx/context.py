from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm

def nav(request):
  blog_sublinks = [
    {'name': 'Blog Home', 'url': '/blog/'},
    {'name': 'Add Post', 'url': '/blog/admin/add/'},
    {'name': 'My Posts', 'url': '/blog/%s/'%request.user.username},
    ]
  _nav = [
    {"name": "Classes",
     "url": "/classes/",
     'sublinks': [
        {"name": "All classes", "url": "/classes/"},
        {"name": "My classes", "url": "/classes/my-sessions/"},
        ]
     },
    {"name": "Blog",
     "url": "/blog/",
     "sublinks": blog_sublinks if request.user.is_staff else [],
     },
    {'name': "Join us", "url": "/join-us/"},
    ]

  return dict(
    current = request.path.split('/')[1] or 'home',
    nav = _nav,
    STATIC_URL = settings.STATIC_URL,
    auth_form = AuthenticationForm,
    app_path = "/admin/login/",
    next = request.path,
    settings = settings,
    )
