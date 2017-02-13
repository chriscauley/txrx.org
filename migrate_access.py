import os, django; os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings';django.setup()

from event.models import Event, Access

accesses = [
  {
    "name": "Open To The Public",
    "icon": "public",
    "order": 0
  },
  {
    "name": "Private - Invitation only",
    "icon": "private",
    "order": 1
  },
  {
    "name": "RSVP Required",
    "icon": "rsvp",
    "order": 2
  }
]

for a in accesses:
  Access.objects.get_or_create(**a)

for event in Event.objects.all():
  event.access = Access.objects.get(icon=event.icon or "public")
  event.save()
