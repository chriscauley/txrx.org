from django.core.mail import send_mail
from django.conf import settings

def filter_emails(emails):
  if settings.DEBUG:
    #only email certain people from dev server!
    return [e for e in emails if e in getattr(settings,'ALLOWED_EMAILS',[])]
  return emails

def filter_users(users):
  if settings.DEBUG:
    #only email certain people from dev server!
    return users.filter(email__in=getattr(settings,'ALLOWED_EMAILS',[]))
  return users

def mail_admins_plus(subject,message,recipient_list=[],from_email=None):
  recipient_list += [email for name,email in settings.ADMINS if not email in recipient_list]
  recipient_list = filter_emails(recipient_list)
  from_email = from_email or settings.DEFAULT_FROM_EMAIL
  if not recipient_list:
    print message
    return
  send_mail(subject,message,from_email,recipient_list)

def send_mail_plus(subject,message,from_email,recipient_list):
  recipient_list = filter_emails(recipient_list)
  if not recipient_list:
    print message
    return
  send_mail(subject,message,from_email,recipient_list)
