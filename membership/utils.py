from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from .models import LimitedAccessKey

import datetime

def limited_login_required(function):
  """
  Like login required, but can use a LimitedAccessKey in place of an actual login.
  """
  def wrap(request, *args, **kwargs):
    if request.user.is_authenticated():
      request.limited_user = request.user
      return function(request, *args, **kwargs)
    if 'LA_KEY' in request.GET:
      try:
        key = LimitedAccessKey.objects.get(key=request.GET['LA_KEY'])
        if key.expires > datetime.date.today():
          # key is good, send it through
          request.limited_user = key.user
          return function(request,*args,**kwargs)
        messages.error(request,"The link you have attempted to use has expired. Please log in to continue.")
      except LimitedAccessKey.DoesNotExist:
        pass
    return HttpResponseRedirect(settings.LOGIN_URL+"?next=%s"%request.path)

  wrap.__doc__=function.__doc__
  wrap.__name__=function.__name__
  return wrap

def user_from_email(email):
  try:
    return User.objects.get(email=email)
  except User.DoesNotExist:
    pass
  try:
    return User.objects.get(usermembership__paypal_email=email)
  except:
    pass

def verify_unique_email(email,user=None):
  """
  Check to make sure that there are no other users with this email.
  Can be used with email or username.
  """
  other_users = User.objects.all()
  if not email:
    return True
  email = email.strip()
  if user:
    other_users = User.objects.exclude(pk=user.pk)
  by_email = other_users.filter(email=email)
  by_username = other_users.filter(username=email)
  by_paypal_email = other_users.filter(usermembership__paypal_email=email)
  return not (by_email or by_username or by_paypal_email)
