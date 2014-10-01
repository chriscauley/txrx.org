from django.conf import settings
from django.contrib.auth import get_user_model

from membership.models import UserMembership
from txrx.utils import reset_password
import random

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
