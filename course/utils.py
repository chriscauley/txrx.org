from django.conf import settings
from django.core.mail import mail_admins
from django.contrib.auth import get_user_model
from django import forms

from lablackey.utils import reset_password
import random, os, json

def validate_email(s):
  f = forms.EmailField()
  try:
    f.clean(s)
    return True
  except forms.ValidationError:
    pass

def get_or_create_student(params,send_mail=True):
  if isinstance(params,(str,unicode)):
    params = {'payer_email': params}
  paypal_email = params.get('payer_email',None)
  email = params.get("email",paypal_email)
  u_id = params.get('custom',None)
  subscr_id = params.get('subscr_id',None) or params.get('recurring_payment_id',None)
  user, new = _get_or_create_student(email,u_id=u_id,subscr_id=subscr_id,send_mail=send_mail)
  if new:
    template_name = params.get("template_name","welcome_classes")
    kwargs = dict(
      subject_template_name="email/%s.subject"%template_name,
      email_template_name="email/%s.html"%template_name
    )
    user.set_password(params.get("password",settings.NEW_STUDENT_PASSWORD))
    user.save()
    if send_mail:
      reset_password(user,**kwargs)
  user.active = True
  user.first_name = user.first_name or params.get("first_name",'')
  user.last_name = user.last_name or params.get("last_name",'')
  user.paypal_email = user.paypal_email or paypal_email # they can set this if they want
  user.save()
  return user, new

def _get_or_create_student(paypal_email,u_id=None,subscr_id=None,send_mail=True):
  email = paypal_email
  User = get_user_model()
  user, new = None, False
  if subscr_id:
    try:
      return User.objects.get(subscription__subscr_id=subscr_id), False
    except User.DoesNotExist:
      pass
  if str(u_id).isdigit():
    user = User.objects.get(id=u_id)
    return user, new
  user = User.objects.get_from_anything(paypal_email)
  if user:
    return user, new
  if validate_email(str(u_id)):
    email = u_id
  username = email.split("@")[0]
  if User.objects.filter(username=username):
    # iff the username is taken, use this instead:
    username = username + str(random.randint(1000,10000))
  return User.objects.get_or_create(email=email,defaults={'username':username})
