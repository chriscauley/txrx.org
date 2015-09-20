import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
import django
django.setup()

from user.models import User

emails = [
  'jon.cordingley@gmail.com',
  'daniel.d.steck@gmail.com',
  'kalexander@porterhedges.com',
  'angelcastellano@yahoo.com',
  'alancablejewelry@gmail.com',
]

for email in emails:
  um = User.objects.get(email=email).usermembership
  if um.orientation_status == "oriented":
    um.send_welcome_email()
    print um.orientation_status
