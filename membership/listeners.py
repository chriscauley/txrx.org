from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from codrspace.models import Setting, Profile
from .models import UserMembership


@receiver(post_save,sender=User)
def post_save_user_handler(sender, **kwargs):
  user = kwargs['instance']
  for model in [Setting,Profile,UserMembership]:
    try:
      model.objects.get(user=user)
    except model.DoesNotExist:
      obj = model(user=user)
      obj.save()
