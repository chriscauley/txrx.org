from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.conf import settings
from txrx.utils import reset_password
import random
import string

class Command(BaseCommand):
  def handle(self, *args, **options):
    new_users = [u for u in User.objects.all() if u.check_password(settings.NEW_STUDENT_PASSWORD)]
    for u in new_users:
      reset_password(u,email_template_name="email/welcome_classes.html")
