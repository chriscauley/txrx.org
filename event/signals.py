from django.db.models.signals import post_save

from codrspace.models import SetPhoto, Photo
from instagram.models import InstagramPhoto
from .models import EventOccurrence

import datetime

def instagram_occurrence_connection(sender, **kwargs):
  obj = kwargs['instance']
  if not obj.approved: # non approved photos should NEVER appear on the site
    Photo.objects.filter(instagramphoto=obj).delete()
    return
  #get all events that started no more than 4 hours before the photo was submitted
  gte = obj.datetime - datetime.timedelta(.5)
  lte = obj.datetime
  occurrences = EventOccurrence.objects.filter(start__lte=lte,start__gte=gte)
  if not occurrences:
    return
  occurrence = occurrences[0]
  defaults = {
    'filename': str(obj.standard_resolution).split('/')[-1],
    'name': obj.name,
    'file': obj.standard_resolution,
    'caption': obj.caption,
    }
  if obj.instagram_user:
    defaults['user'] = obj.instagram_user.user
  photo,new = Photo.objects.get_or_create(instagramphoto=obj,defaults=defaults)
  photoset = occurrence.get_or_create_photoset()
  setphoto,new = SetPhoto.objects.get_or_create(photo=photo,photoset=photoset)

def twitter_occurrence_connection(sender,**kwargs):
  pass

post_save.connect(instagram_occurrence_connection, sender=InstagramPhoto)
