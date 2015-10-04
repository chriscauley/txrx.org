from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User

@receiver(post_save,sender=User)
def post_save_user_handler(sender, **kwargs):
  from membership.models import UserMembership
  user = kwargs['instance']
  UserMembership.objects.get_or_create(user=user)
