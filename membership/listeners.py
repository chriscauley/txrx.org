from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserMembership


@receiver(post_save,sender=User)
def post_save_user_handler(sender, **kwargs):
  user = kwargs['instance']
  UserMembership.objects.get_or_create(user=user)
