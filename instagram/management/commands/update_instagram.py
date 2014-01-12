from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

from simplejson import loads
import requests, os

from instagram.models import InstagramTag, InstagramLocation, InstagramUser, InstagramPhoto
from txrx.utils import mail_on_fail

class Command (BaseCommand):
  @mail_on_fail
  def handle(self, *args, **options):
    # InstagramPhoto.objects.all().delete() #useful for testing!
    count = InstagramPhoto.objects.count()
    for model in [InstagramTag, InstagramLocation, InstagramUser]:
      for instance in model.objects.filter(follow=True):
        instance.follow_me()
    new = InstagramPhoto.objects.count()-count
    if new>0:
      mailto = getattr(settings,"INSTAGRAM_EMAIL",settings.ADMINS)
      print "emailing %s to %s"%(new,mailto)
      send_mail(
        "New Instagram Photos",
        "There are %s new instagram photos. Pleas visit the admin to approve them."%new,
        "noreply@txrxlabs.org",
        mailto,
        )
