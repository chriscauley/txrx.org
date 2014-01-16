from django.contrib.auth.models import User
from django.conf import settings
from membership.models import UserMembership
from txrx.utils import reset_password

def get_or_create_student(email):
  try:
    user = User.objects.get(usermembership__paypal_email=email)
  except User.DoesNotExist:
    user, new = User.objects.get_or_create(email=email,defaults={'username':email[:30]})
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
  return user
