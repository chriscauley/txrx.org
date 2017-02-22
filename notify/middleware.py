from django.utils import timezone

from notify.models import Notification

class MarkNotificationReadMiddleware(object):
  def process_request(self,request):
    if request.user.is_authenticated():
      Notification.objects.filter(user=request.user,url=request.path).update(read=timezone.now())
