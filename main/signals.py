from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

from mptt_comments.models import MpttComment

def mail_admins_plus(subject,message,recipient_list):
  recipient_list += [email for name,email in settings.ADMINS if not email in recipient_list]
  send_mail(
    subject,
    message,
    settings.DEFAULT_FROM_EMAIL,
    recipient_list)

def new_comment_connection(sender, instance=None, created=False,**kwargs):
  if not created:
    return
  admin_url = settings.ROOT_URL + reverse('admin:mptt_comments_mpttcomment_change',args=[instance.id])
  try:
    object_url = settings.ROOT_URL + instance.content_object.get_absolute_url()
  except AttributeError:
    object_url = settings.ROOT_RL + instance.get_absolute_url()
  try:
    users = [user.email for user in instance.content_object.list_users]
  except AttributeError:
    users = []
  body = "A new comment has been added to the TXRX Labs website.\n\n"
  body += "View comment on site: %s \n\n"%object_url
  body += "Edit/delete comment: %s \n\n"%admin_url
  body += "Comment content:\n\n%s"%instance.comment
  mail_admins_plus('New Comment',body,users)

post_save.connect(new_comment_connection, sender=MpttComment)
