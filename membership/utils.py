from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse

from .models import LimitedAccessKey
from lablackey.mail import send_template_email
from lablackey.utils import get_or_none

import datetime

def send_membership_email(*args,**kwargs):
  kwargs['from_email'] = settings.MEMBERSHIP_EMAIL
  send_template_email(*args,**kwargs)

def temp_user_required(function):
  """
  Like login required, but can store a users id in place of a login. Used for kiosks.
  Should only be used for ajax requests.
  Will add request.temp_user or return {'errors': {'non_field_error': message }} or {'next': url}
  """
  def wrap(request,*args,**kwargs):
    expiration_time = 5*60
    if request.user.is_authenticated():
      request.temp_user = request.user
      return function(request,*args,**kwargs)

    User = get_user_model()
    if request.session.get('temp_user_id',None):
      request.temp_user = User.objects.get(id=request.session['temp_user_id'])
      request.session.set_expiry(expiration_time)
      return function(request,*args,**kwargs)
    rfid = request.POST.get('rfid',None)
    user = get_or_none(User,rfid__number=rfid or 'notavalidrfid')
    email = request.POST.get("email",None) or "notavaildemail"
    if not user and email and 'password' in request.POST:
      user = User.objects.get_from_anything(email)
      if user and not user.check_password(request.POST['password']):
        return JsonResponse({'errors': {'non_field_error': 'Username and password do not match, please try again'}},
                            status=401)
    if user:
      request.temp_user = user
      request.session['temp_user_id'] = user.id
      request.session.set_expiry(expiration_time)
      return function(request,*args,**kwargs)
    if rfid:
      return JsonResponse({'next': "new-rfid", 'rfid': rfid})
    return JsonResponse({'errors': {'non_field_error': 'Unable to find user. Contact the staff'}},
                        status=401)

  wrap.__doc__=function.__doc__
  wrap.__name__=function.__name__
  return wrap

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
    return User.objects.get(paypal_email=email)
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
  by_paypal_email = other_users.filter(paypal_email__iexact=email)
  return not (by_email or by_username or by_paypal_email)
