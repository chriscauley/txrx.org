#! TODO: this should be a part of unrest_comments, and should be optional
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, mail_admins
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models.signals import post_save

from unrest_comments.models import UnrestComment

from membership.models import LimitedAccessKey
from notify.models import Notification
from .var import admin_comment_email, comment_response_email

_u = lambda s: settings.SITE_URL + s

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

  try:
    url = instance.content_object.get_absolute_url()
  except AttributeError:
    url = None
  _kwargs = {
    'target_type': 'unrest_comments.unrestcomment',
    'target_id': instance.id,
    'url': url,
    'emailed': timezone.now(),
  }
  if instance.parent:
    # email whoever wrote the parent comment
    user = instance.parent.user
    Notification.objects.create(
      message='Comment Reply on "%s" from %s'%(instance.content_object,instance.user),
      user=user,
      relationship='comment_reply',
      **_kwargs
    )
    key = LimitedAccessKey.new(user).key
    _dict['unsubscribe_url'] = _u(reverse("unsubscribe",args=['comments',user.id])+"?LA_KEY="+key)
    subject = 'Someone responded to your comment'
    send_mail(
      subject,
      comment_response_email%_dict,
      settings.DEFAULT_FROM_EMAIL,
      [user.email]
    )
  else:
    # email the course instructor or whoever is in the "users" list
    users = list(get_user_model().objects.filter(id__in=getattr(settings,'COMMENT_ADMIN_IDS',[])))
    try:
      users += instance.content_object.list_users
    except AttributeError:
      pass
    users = set(users)
    if True:
      return
    for user in users:
      Notification.objects.create(
        message='New comment on %s from %s'%(instance.content_object,instance.user),
        user=user,
        relationship='new_comment',
        **_kwargs
      )
      subject = 'New comment on %s'%instance.content_object
      send_mail(subject,admin_comment_email%_dict,settings.DEFAULT_FROM_EMAIL,[user.email])

post_save.connect(new_comment_connection, sender=UnrestComment)
