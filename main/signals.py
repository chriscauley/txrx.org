from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

from mptt_comments.models import MpttComment

from membership.models import UnsubscribeLink
from .var import admin_comment_email, comment_response_email

_u = lambda s: settings.SITE_URL + s

def mail_admins_plus(subject,message,recipient_list):
  recipient_list += [email for name,email in settings.ADMINS if not email in recipient_list]
  send_mail(
    subject,
    message,
    settings.DEFAULT_FROM_EMAIL,
    recipient_list)

def new_comment_connection(sender, instance=None, created=False,**kwargs):
  if not created or settings.DEBUG:
    return
  _dict = {
    'content': instance.comment,
    'admin_url': _u(reverse('admin:mptt_comments_mpttcomment_change',args=[instance.id])),
    'object_name': instance.content_object,
    'admin_email': settings.ADMINS[0][1],
    }

  try:
    _dict['object_url'] = _u(instance.content_object.get_absolute_url()) + "#c%s"%instance.id
  except AttributeError:
    _dict['object_url'] = _u(instance.get_absolute_url())

  if instance.parent:
    # email whoever wrote the parent comment
    user = instance.parent.user
    if user.usermembership.notify_comments and user.usermembership.notify_global:
      # this conditional is incase they opt out
      _dict['unsubscribe_url'] = _u(UnsubscribeLink.new(user).get_absolute_url())
      users = []
      subject = 'Someone responded to your comment'
      send_mail(
        subject,
        comment_response_email%_dict,
        settings.DEFAULT_FROM_EMAIL,
        [user.email])
  else:
    # email the course instructor or whoever is in the "users" list
    try:
      users = [user.email for user in instance.content_object.list_users]
    except AttributeError:
      users = []

  mail_admins_plus('New Comment',admin_comment_email%_dict,users)

post_save.connect(new_comment_connection, sender=MpttComment)
