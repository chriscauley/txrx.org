from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

class Command(BaseCommand):
  def handle(self, *args, **options):
    User = get_user_model()
    from membership.models import UserMembership
    password = None
    user_list = [u.username for u in User.objects.order_by('id')]
    for u in User.objects.using('anon').all():
      u.username = 'user__%s'%u.id
      u.first_name = ""
      u.last_name = ""
      u.email = 'user__%s@example.com'%u.id
      if password:
        u.password = password
      else:
        u.set_password('hackerspace')
        password = u.password
      u.save()
    u=User.objects.using('anon').filter(is_superuser=True)[0]
    u.username='admin'
    u.save()
    User.objects.all().update(paypal_email=None)
    if options.get("verbosity") > 0:
      print "%s users with normal emails"%User.objects.using('anon').exclude(email__startswith="user__").count()
      print "%s users with normal names"%User.objects.using('anon').exclude(username__startswith="user__").count()
      print "%s users with paypal emails"%User.objects.using('anon').filter(usermembership__isnull=True).count()
    if user_list != [u.username for u in User.objects.order_by('id')]:
      raise NotImplementedError('print user table has been altered!')
    
