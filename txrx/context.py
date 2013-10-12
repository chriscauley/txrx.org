from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from tagging.models import Tag

from event.models import EventOccurrence
from course.models import ClassTime, Enrollment

import datetime,time

def nav(request):
  blog_sublinks = [
    {'name': 'Blog Home', 'url': '/blog/', 'pjax': True},
    {'name': 'Add Post', 'url': '/blog/admin/add/'},
    {'name': 'My Posts', 'url': '/blog/%s/'%request.user.username},
    ]
  about_links = [
    {'name': 'About TX/RX', 'url': '/about-us/'},
    {'name': 'Bylaws', 'url': '/bylaws/'},
    {'name': 'Meeting Minutes', 'url': '/minutes/'},     
    ]
  _nav = [
    {"name": "Classes",
     "url": "/classes/",
     #'sublinks': [
     #   {"name": "All classes", "url": "/classes/", 'pjax': False},
     #   {"name": "My classes", "url": "/classes/my-sessions/", 'pjax': True},
     #   ]
     },
    {"name": "Blog",
     "url": "/blog/",
     'pjax': True,
     "sublinks": blog_sublinks if request.user.is_staff else [],
     },
    {'name': "Join us", "url": "/join-us/", 'pjax': True},
    {'name': "Location", "url": "/map/", 'pjax': True},
    {'name': "Events", "url": "/event/", 'pjax': False},
    {"name": "Information",
     "url": "/about-us/",
     "sublinks": about_links,
     },
    ]
  now = datetime.datetime.now()

  class_faqs = [
    ('Do I have to create an account? No!','When you register classes, an account will be created at txrxlabs.org using your email address. You will be emailed login credentials. Most people who take classes with us just ignore this email, and that is fine.'),
    ('Can I pay cash? Sure!', 'Come to the lab in person and ask to see Roland or any officer. They can accept payment and give you a receipt. Some classes do have an enrollment cap, so it is better to do this sooner than later.'),
    ('Is this class right for me? Maybe...','Most classes are for beginners, and clicking on the class title will take you to the class detail page. The right column shows <span class="has_notes">prerequisites</span> and <span class="has_notes">requirements</span>. If you mouse over them you will see what is required for that class. Some classes require a brief <span class="has_notes">safety</span> class which is taught 20 minutes before the class. Additionally, there may be <span class="has_notes">fee notes</span> which explain how much of the cost goes towards materials.'),
    ]

  return dict(
    current = request.path.split('/')[1] or 'home',
    nav = _nav,
    STATIC_URL = settings.STATIC_URL,
    auth_form = AuthenticationForm,
    app_path = "/admin/login/",
    settings = settings,
    upcoming_events = EventOccurrence.objects.filter(start__gte=now,start__lte=now+datetime.timedelta(7)),
    #last_week = EventOccurrence.objects.filter(start__lte=now,photoset__isnull=False),
    tags = Tag.objects.all(),
    class_faqs = class_faqs,
    all_ics = '%s/event/ics/all_events.ics'%settings.SITE_DOMAIN, #! move to event.context
    google_calendar_url = 'http://www.google.com/calendar/render?cid=', #! move to event.context
    all_classes_ics = '%s/classes/ics/all_classes.ics'%settings.SITE_DOMAIN, #! move to course.context
    )

def evaluations(request):
  _e = Enrollment.objects.pending_evaluation(user=request.user)
  print _e
  return {'pending_evaluations': _e}

def motd(request):
  if True:
    return {}
  now = time.time()
  yesterday = now - 60*60*24
  if request.session.get('last_MOTD',0) > yesterday or settings.DEBUG:
    # They have seen a MOTD in the past 24 hours, don't show them one
    return {}
  request.session['last_MOTD'] = now
  request.session.save()

  today = datetime.date.today()
  tomorrow = today + datetime.timedelta(1)
  events = EventOccurrence.objects.filter(start__gte=today,start__lte=tomorrow)
  class_times = ClassTime.objects.filter(start__gte=today,start__lte=tomorrow)
  if not classes or not events:
    return {}

  messages.success(request,"hooray message of the day")
  return {}
