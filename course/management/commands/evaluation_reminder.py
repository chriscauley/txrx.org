from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.loader import render_to_string

from course.models import Enrollment
from txrx.utils import print_to_mail
from membership.models import LimitedAccessKey

import datetime

class Command (BaseCommand):
  @print_to_mail(subject="[LOG] Evaluation Reminder")
  def handle(self, *args, **options):
    yesterday = datetime.datetime.now()-datetime.timedelta(1)
    pe = Enrollment.objects.pending_evaluation()
    pe = pe.filter(evaluation_date__gte=yesterday)
    if pe.count:
      print "sending %s evaluation emails"%pe.count()
    for evaluation in pe:
      if not evaluation.user.email:
        continue
      _dict = {
        'evaluation': evaluation,
        'la_key': LimitedAccessKey.new(evaluation.user),
        'domain': settings.SITE_URL
      }
      send_mail(
        "Please evaluate the class you took from TX/RX",
        render_to_string("email/pending_evaluation.html",_dict),
        settings.DEFAULT_FROM_EMAIL,
        [evaluation.user.email]
      )
      print "Emailed %s about %s"%(evaluation.email,evaluation.session)
