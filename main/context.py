from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import connection
from django.db.models import Q

from tagging.models import Tag

from blog.models import PressItem
from course.models import ClassTime, Enrollment
from course.views.ajax import get_needed_sessions
from membership.models import Container
from event.models import EventOccurrence
from redtape.models import Signature
import datetime, time

_materials = lambda: get_needed_sessions().filter(needed_completed__isnull=True).count()
_containers = lambda: Container.objects.filter(Q(status='maintenance')|Q(status='canceled')).count()
def _orientations():
  start = datetime.date.today()
  end = start + datetime.timedelta(1)
  _os = EventOccurrence.objects.filter(start__gte=start,start__lte=end,event_id=settings.ORIENTATION_EVENT_ID)
  count = 0
  for _o in _os:
    count += _o.get_rsvps().count()
  return count

def get_upcoming_events():
  now = datetime.datetime.now()
  kwargs = dict(start__gte=now,start__lte=now+datetime.timedelta(7))
  e = EventOccurrence.objects.filter(event__hidden=False,**kwargs)
  c = ClassTime.objects.filter(session__active=True,**kwargs)
  return sorted(list(c)+list(e),key=lambda o:o.start)

def get_calendar_sublinks(request):
  one_week = datetime.date.today()+datetime.timedelta(7)
  occurrences = EventOccurrence.objects.filter(event__eventowner__user=request.user,start__lte=one_week)
  occurrences = occurrences.filter(start__gte=datetime.datetime.today())
  out = [{
    'name': "<b>%s</b> %s"%(o.verbose_start,o.event.get_short_name()),
    'url': "/tools/master/event/rsvp/?object_id=%s"%o.id,
    'reddot': o.total_rsvp
    } for o in occurrences]
  if out:
    out = [{'name': "View All",'url': '/event/'}] + out
  return out

def nav(request):
  blog_sublinks = [
    {'name': 'Blog Home', 'url': '/blog/'},
    {'name': 'Add Post', 'url': '/blog/admin/add/'},
    {'name': 'My Posts', 'url': '/blog/%s/'%request.user.username},
  ]
  about_links = []
  is_superuser = request.user.is_superuser
  if request.user.is_authenticated():
    about_links = [
      {'name': 'About TXRX', 'url': '/about-us/'},
      {'name': 'Bylaws', 'url': '/bylaws/'},
      {'name': 'Meeting Minutes', 'url': '/minutes/'},
      {'name': 'Google Groups (Public)', 'url': 'https://groups.google.com/forum/#!forum/txrxlabs'},
      {'name': 'Google Groups (Members)', 'url': 'https://groups.google.com/forum/#!forum/txrxmembership'},
      {'name': 'Membership Handbook (PDF)', 'url': '/static/handbook.pdf'},
    ]
    # only oriented users get to see the orientation notes.
    if request.user.usercriterion_set.filter(criterion_id=15).count():
      about_links.append({
        'name': 'Orientation Notes',
        'url': 'https://docs.google.com/document/d/1Cb-83FJ_8n_ModIIRMGesTOTfefoeVA2V--s-5XWa_M/edit?ts=56ca03d5',
      })
  social_nav = [
    {'name': 'facebook','url': 'https://www.facebook.com/TxRxLabs' },
    {'name': 'twitter','url': 'https://twitter.com/txrxlabs' },
    {'name': 'instagram','url': 'https://instagram.com/txrxlabs/' },
  ]
  tool_sublinks = []
  # if request.user.is_authenticated():
  #   tool_sublinks = [
  #     {'name': 'Tools','url': '/tools/'},
  #     {'name': 'Checkout Items', 'url': '/tools/checkout-items/'},
  #   ]

  if getattr(request.user,'is_toolmaster',False) or is_superuser:
    tool_sublinks += [
      {'name': 'Tools','url': '/tools/'},
      {'name': 'Checkout Items', 'url': '/tools/checkout-items/'},
      {'name': 'Permissions','url': '/toolmaster'},
      {'name': 'Materials Needed','url': '/needed-sessions/','reddot': _materials },
      {'name': 'Orientations','url': '/event/orientations/','reddot': _orientations },
      {'name': 'Bays + Tables', 'url': '/admin/membership/container/?needs+Staff=yes&o=2', 'reddot': _containers},
    ]
  if request.user.is_authenticated() and (request.user.is_staff or request.user.is_volunteer):
    tool_sublinks.append({"name": "Today's Checkins",'url': '/todays-checkins'})
  if getattr(request.user,'is_gatekeeper',False) or is_superuser:
    tool_sublinks.append({'name': 'RFID Table','url': '/rfid_permission_table/'})
  if request.user.is_authenticated() and request.user.subscription_set.filter(canceled__isnull=True):
    _l = 'https://docs.google.com/document/d/1Cb-83FJ_8n_ModIIRMGesTOTfefoeVA2V--s-5XWa_M/edit?usp=sharing'
    about_links.append({'name': 'Orientation Notes','url': _l})
  _nav = [
    {"name": "About",
     "url": "/about-us/",
     "sublinks": about_links if request.user.is_authenticated() else [],
     },
    {"name": "Classes",
     "url": "/classes/",
     },
    {'name': "Tools",
     "url": "/tools/",
     "sublinks": tool_sublinks,
    },
    {"name": "Blog",
     "url": "/blog/",
     "sublinks": blog_sublinks if request.user.is_staff else [],
     },
    {'name': "Calendar",
     "url": "/event/",
     "class": "calendar",
     "sublinks": get_calendar_sublinks(request) if request.user.is_staff else [],
     },
    #{'name': "Facility", "url": "/facility/"},
    {'name': "Membership", "url": "/join-us/"},
    {'name': "Contact", "url": "/map/"},
    {'name': "Shop", "url": "/shop/"},
    {'name': "FAQ", "url": "/faq/"},
    {'name': "Services",
     "url": "/work/",
     "sublinks": [
       { "name": "Work", "url": "/work/" },
       { "name": "Photo Studio", "url": "/photo-studio/" },
     ]
    },
  ]

  for _n in _nav:
    if request.path.startswith(_n['url']):
      _n['class'] = _n.get("class","")+' current'
  now = datetime.datetime.now()

  class_faqs = [
    ('Do I have to create an account? No!','When you register classes, an account will be created at txrxlabs.org using your email address. You will be emailed login credentials. Most people who take classes with us just ignore this email, and that is fine.'),
    ('Can I pay cash? Sure!', 'Come to the lab in person and ask to see Roland or any officer. They can accept payment and give you a receipt. Some classes do have an enrollment cap, so it is better to do this sooner than later.'),
    ('Is this class right for me? Maybe...','Most classes are for beginners, and clicking on the class title will take you to the class detail page. The right column shows <span class="has_notes">prerequisites</span> and <span class="has_notes">requirements</span>. If you mouse over them you will see what is required for that class. Some classes require a brief <span class="has_notes">safety</span> class which is taught 20 minutes before the class. Additionally, there may be <span class="has_notes">fee notes</span> which explain how much of the cost goes towards materials.'),
    ]

  my_classes_ics = None
  documents_needed = 0
  if request.user.is_authenticated():
    my_classes_ics = "%s/classes/ics/%s/%s/my-classes.ics"
    my_classes_ics = my_classes_ics%(settings.SITE_DOMAIN,request.user.id,request.user.usermembership.api_key)
    if settings.DEBUG:
      d_ids = getattr(settings,"REQUIRED_DOCUMENT_IDS",[])
      documents_needed = len(d_ids) - Signature.objects.filter(document_id__in=d_ids,user=request.user).count()

  login_redirect = request.path
  if 'auth' in request.path or 'accounts' in request.path:
    login_redirect = "/"

  return dict(
    documents_needed = documents_needed,
    current = request.path.split('/')[1] or 'home',
    nav = _nav,
    social_nav = social_nav,
    STATIC_URL = settings.STATIC_URL,
    auth_form = AuthenticationForm,
    app_path = "/admin/login/",
    settings = settings,
    upcoming_events = get_upcoming_events,
    #last_week = EventOccurrence.objects.filter(start__lte=now,photoset__isnull=False),
    tags = Tag.objects.all(),
    class_faqs = class_faqs,
    my_classes_ics = my_classes_ics,
    all_ics = '%s/event/ics/all_events.ics'%settings.SITE_DOMAIN, #! move to event.context
    calendar_protocols = ['http://www.google.com/calendar/render?cid=http://','webcal://'], #! move to event.context
    all_classes_ics = '%s/classes/ics/all_classes.ics'%settings.SITE_DOMAIN, #! move to course.context
    pressitems = PressItem.objects.all(),
    login_redirect = login_redirect,
    SITE_DOMAIN = "https://txrxlabs.org",
    sql_time_sum = lambda: sum([float(q['time'])*1000 for q in connection.queries]),
  )

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
