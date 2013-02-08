from django.db.models.signals import post_save

from codrspace.models import SetPhoto
from instagram.models import InstagramPhoto
from .models import EventOccurrence

import datetime

def instagram_occurrence_connection(sender, **kwargs):
  obj = kwargs['instance']
  if not obj.approved:
    return
  #get all events that started no more than 4 hours before the photo was submitted
  gte = obj.datetime - datetime.timedelta(.5)
  lte = obj.datetime
  occurrences = EventOccurrence.objects.filter(start__lte=lte,start__gte=gte)
  if not occurrences:
    return
  occurrence = occurrences[0]
  photoset = occurrence.get_photoset()
  setphoto,new = SetPhoto.objects.get_or_create(instagram_photo=obj,photoset=photoset)
  if new:
    print "Set Photo Created"

def twitter_occurrence_connection(sender,**kwargs):
  pass

post_save.connect(instagram_occurrence_connection, sender=InstagramPhoto)
