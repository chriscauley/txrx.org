from django.contrib.auth.models import User

def user_from_email(email):
  try:
    return User.objects.get(email=email)
  except User.DoesNotExist:
    pass
  try:
    return User.objects.get(usermembership__paypal_email=email)
  except:
    pass
