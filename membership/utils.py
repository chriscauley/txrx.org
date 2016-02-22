from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import LimitedAccessKey
from lablackey.mail import send_template_email

import datetime

def send_membership_email(*args,**kwargs):
  kwargs['from_email'] = settings.MEMBERSHIP_EMAIL
  send_template_email(*args,**kwargs)

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
  user = get_user_model()
  try:
    return User.objects.get(email=email)
  except User.DoesNotExist:
    pass
  try:
    return User.objects.get(usermembership__paypal_email=email)
  except:
    pass

def verify_unique_email(email,user=None):
  if not email:
    return True
  other_users = get_user_model().objects.all()
  email = email.strip()
  if user:
    other_users = other_users.exclude(pk=user.pk)
  by_email = other_users.filter(email__iexact=email)
  by_username = other_users.filter(username__iexact=email)
  by_paypal_email = other_users.filter(usermembership__paypal_email__iexact=email)
  return not (by_email or by_username or by_paypal_email)
