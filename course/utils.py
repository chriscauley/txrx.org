from django.conf import settings
from django.core.mail import mail_admins
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from membership.models import UserMembership
from txrx.utils import reset_password
import random, os, json

def get_or_create_student(email,u_id=None):
  User = get_user_model()
  new = False
  if str(u_id).isdigit():
    user = User.objects.get(id=u_id)
    profile = user.usermembership
    profile.email = email
    profile.save()
    return user,new
  try:
    user = User.objects.get(usermembership__paypal_email=email)
  except User.DoesNotExist:
    username = email.split("@")[0]
    if User.objects.filter(username=username):
      # iff the username is taken, use this instead:
      username = username + str(random.randint(1000,10000))
    user, new = User.objects.get_or_create(email=email,defaults={'username':username})
    if new:
      profile = user.usermembership
      profile.paypal_email=profile.paypal_email or email
      profile.save()
      kwargs = dict(
        subject_template_name="email/welcome_classes_subject.txt",
        email_template_name="email/welcome_classes.html"
        )
      user.set_password(settings.NEW_STUDENT_PASSWORD)
      user.save()
      reset_password(user,**kwargs)
  return user,new

def reset_classes_json(context="no context provided"):
  from course.models import Course, Subject
  values = {
    'courses': json.dumps([c.as_json for c in Course.objects.filter(active=True)]),
    'subjects': json.dumps([s.as_json for s in Subject.objects.filter(parent=None)]),
  }
  text = render_to_string('course/classes.json',values)
  f = open(os.path.join(settings.STATIC_ROOT,'classes.json'),'w')
  f.write(text)
  f.close()

  # for now email chris whenever this happens so that he can check
  # if it's firing too often or during a request
  mail_admins("classes.json reset",context)
