from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
_nav = [
  {"name": "all classes",
   "url": "/classes/",
   'sublinks': [
      ]
   },
  {"name": "my classes", "url": "/classes/my-sessions/"},
  #{"name": "blog", "url": "/weblog/"}
  ]

def nav(request):
  return dict(
    current = request.path.split('/')[1] or 'home',
    nav = _nav,
    STATIC_URL = settings.STATIC_URL,
    auth_form = AuthenticationForm,
    app_path = "/admin/login/",
    next = request.path,
    settings = settings,
    )
