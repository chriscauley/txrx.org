from django.conf import settings
from django.core.management.base import BaseCommand

from course.models import Enrollment
from redtape.models import Signature

import datetime

class Command(BaseCommand):
  def handle(self,*args,**kwargs):
    for enrollment in Enrollment.objects.all():
      enrollment.save()
    for signature in Signature.objects.all():
      signature.save()
