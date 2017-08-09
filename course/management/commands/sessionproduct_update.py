from django.conf import settings
from django.core.mail import mail_admins
from django.core.management.base import BaseCommand
from django.utils import timezone

from course.models import Session

class Command(BaseCommand):
  def handle(self, *args, **options):
    lines = []
    for session in Session.objects.filter(active=True,first_date__gte=timezone.now()):
      session.save()
      lines.append("%s was bad"%session)
    if lines:
      pass #mail_admins("bad sessions","\n".join(lines))
