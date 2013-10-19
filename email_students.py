"""A one off script for converting between the old and new alert system. A lot of students were missed because I wasn't sending emails"""
from django.contrib.auth.models import User
from django.conf import settings
from txrx.utils import reset_password
import datetime

_dt = datetime.datetime.now()-datetime.timedelta(120)
users = User.objects.filter(last_login__gte=_dt,date_joined__gte=_dt)
users = [u for u in users if u.last_login == u.date_joined]
new_users = [u for u in users if u.check_password(settings.NEW_STUDENT_PASSWORD)]
print "emailing: %s"%len(new_users)
if False:
  for u in new_users:
    print u
    reset_password(u,email_template_name="email/welcome_classes.html",subject_template_name="email/welcome_classes_subject.txt")
