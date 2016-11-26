from django.conf import settings
from django.core.mail import send_mail, mail_admins
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

from unrest_comments.models import UnrestComment

from membership.models import LimitedAccessKey
from .var import admin_comment_email, comment_response_email

_u = lambda s: settings.SITE_URL + s

comment_admins = getattr(settings,"COMMENT_ADMINS",[settings.ADMINS[0][1]])

def new_comment_connection(sender, instance=None, created=False,**kwargs):
  if not created:
    return
  _dict = {
    'content': instance.comment,
    'admin_url': _u(reverse('admin:unrest_comments_unrestcomment_change',args=[instance.id])),
    'object_name': instance.content_object,
    'admin_email': settings.ADMINS[0][1],
    }

  try:
    _dict['object_url'] = _u(instance.content_object.get_absolute_url()) + "#c%s"%instance.id
  except AttributeError:
    _dict['object_url'] = _u(instance.get_absolute_url())
  users = []

  if instance.parent:
    # email whoever wrote the parent comment
    user = instance.parent.user
    if user.usermembership.notify_comments and user.usermembership.notify_global:
      # this conditional is incase they opt out
      key = LimitedAccessKey.new(user).key
      _dict['unsubscribe_url'] = _u(reverse("unsubscribe",args=['comments',user.id])+"?LA_KEY="+key)
      subject = 'Someone responded to your comment'
      send_mail(
        subject,
        comment_response_email%_dict,
        settings.DEFAULT_FROM_EMAIL,
        [user.email])
  else:
    # email the course instructor or whoever is in the "users" list
    users = getattr(settings,'COMMENT_ADMINS',[])
    try:
      users += [user.email for user in instance.content_object.list_users]
    except AttributeError:
      pass
    subject = 'New comment on %s'%instance.content_object
    send_mail(subject,admin_comment_email%_dict,settings.DEFAULT_FROM_EMAIL,list(set(users)))

post_save.connect(new_comment_connection, sender=UnrestComment)
