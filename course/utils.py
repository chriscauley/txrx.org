from django.contrib.auth.models import User
from django.conf import settings
from membership.models import UserMembership

def get_or_create_student(email):
  try:
    user = User.objects.get(usermembership__paypal_email=email)
  except User.DoesNotExist:
    user, new = User.objects.get_or_create(email=email,defaults={'username':email[:30]})
    if new:
      user.set_password(settings.NEW_STUDENT_PASSWORD)
      user.save()
      profile = user.usermembership
      profile.paypal_email=profile.paypal_email or email
      profile.save()
  return user
