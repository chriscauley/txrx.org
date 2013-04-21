from django.db.models.signals import post_save
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse

from mptt_comments.models import MpttComment

def mptt_comment_connection(sender, **kwargs):
  obj = kwargs['instance']
  url = reverse('admin:mptt_comments_mpttcomment_change',args=[obj.id])
  print url
  mail_admins('New Comment',url)

post_save.connect(mptt_comment_connection, sender=MpttComment)
