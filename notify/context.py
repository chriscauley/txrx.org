from django.conf import settings
from django.utils import timezone

import datetime

def process(request):
  if not request.user.is_authenticated():
    return {}
  request.user.notification_set.filter(read__isnull=True,url=request.path).update(read=timezone.now())
  return {}
  #  'unread_notifications': request.user.notification_set.filter(
  #    read__isnull=True,
  #    datetime__gte=timezone.now()-datetime.timedelta(getattr(settings,"NOTIFICATION_EXPIRY_DAYS",7))
  #  ),
  #}
