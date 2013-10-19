from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.loader import render_to_string

from course.models import Enrollment
from main.signals import send_mail_plus
from membership.models import LimitedAccessKey

import datetime

class Command (BaseCommand):
  def handle(self, *args, **options):
    yesterday = datetime.datetime.now()-datetime.timedelta(1)
    pe = Enrollment.objects.pending_evaluation()
    pe = pe.filter(evaluation_date__gte=yesterday)
    print "sending %s evaluation emails"%pe.count()
    for evaluation in pe:
      _dict = {
        'evaluation': evaluation,
        'la_key': LimitedAccessKey.new(evaluation.user),
        'domain': settings.SITE_URL
        }
      send_mail_plus(
        "Please evaluate the class you took from TX/RX",
        render_to_string("email/pending_evaluation.html",_dict),
        settings.DEFAULT_FROM_EMAIL,
        [evaluation.user.email]
        )
