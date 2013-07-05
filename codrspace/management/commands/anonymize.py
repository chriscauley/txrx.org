from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
  def handle(self, *args, **options):
    from membership.models import UserMembership
    password = None
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
    UserMembership.objects.all().update(paypal_email=None)
    print "%s users with normal emails"%User.objects.using('anon').exclude(email__startswith="user__").count()
    print "%s users with normal names"%User.objects.using('anon').exclude(username__startswith="user__").count()
    print "%s users with paypal emails"%User.objects.using('anon').filter(usermembership__isnull=True).count()
    
