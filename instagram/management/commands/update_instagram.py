from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

from simplejson import loads
import requests, os

from instagram.models import InstagramPhoto, InstagramLocation, photofile_path

InstagramPhoto.objects.all().delete()

tag_url = "https://api.instagram.com/v1/tags/%s/media/recent?access_token=%s"
user_url = "https://api.instagram.com/v1/users/%s/media/recent?access_token=%s&count=100"
user_search_url = "https://api.instagram.com/v1/users/search?q=%s&access_token=%s"
location_search_url = "https://api.instagram.com/v1/locations/search?lat=%s&lng=%s&access_token=%s"
token = getattr(settings,'INSTAGRAM_TOKEN',"3794301.f59def8.e08bcd8b10614074882b2d1b787e2b6f")

def save_photos(response,new,count,approved=False,username=""):
  photo_dir = os.path.join(settings.MEDIA_ROOT,photofile_path)
  if not os.path.exists(photo_dir):
    os.mkdir(photo_dir)
  for item in response['data']: # image dicts
    defaults = dict(
      created_time = item['created_time'],
      approved = approved,
      )
    if item['caption']:
      defaults['username'] = item['caption']['from']['username']
      defaults['caption'] = item['caption']['text']
    else:
      defaults['username'] = username or 'anonymous'
    i,n = InstagramPhoto.objects.get_or_create(iid=item['id'],defaults=defaults)
    new += n; count += 1
    if n: # save photos
      i.location = save_location(item['location'])
      i.save()
      for size in ['thumbnail','low_resolution','standard_resolution']:
        url = item['images'][size]['url']
        print url
        ri = requests.get(url,stream=True)
        path = os.path.join(photo_dir,url.split("/")[-1])
        f = open(path,'w')
        f.write(ri.raw.read())
        f.close()
        setattr(i,size,path.split('media/')[-1])
        i.save()
  return new,count

def save_location(location):
  if not location:
    return
  if 'id' in location:
    location,new = InstagramLocation.objects.get_or_create(iid=location.pop('id'),defaults=location)
    if new:
      print "New Location: %s"%location
    return location
  # search instagram for any locations nearby that are alread in the database
  r = requests.get(location_search_url%(location['latitude'],location['longitude'],token))
  response = loads(r.text)
  for l in response['data']:
    try:
      return InstagramLocation.objects.get(iid=l['id'])
    except InstagramLocation.DoesNotExist:
      pass
  
class Command (BaseCommand):
  def handle(self, *args, **options):
    # InstagramPhoto.objects.all().delete() #useful for testing!
    wxh = lambda img: "%sx%s"%(img['width'],img['height'])
    new,count = 0,0
    tag = getattr(settings,'INSTAGRAM_TAG','')
    userid = getattr(settings,'INSTAGRAM_USERID','')
    username = getattr(settings,'INSTAGRAM_USERNAME','')
    if tag:
      r = requests.get(tag_url%(tag,token))
      response = loads(r.text)
      new,count = save_photos(response,new,count)
    if username and not userid:
      r = requests.get(user_search_url%(username,token))
      response = loads(r.text)
      for user in response['data']:
        if user['username'] == username:
          userid = user['id']
          break
    if userid:
      r = requests.get(user_url%(userid,token))
      response = loads(r.text)
      new,count = save_photos(response,new,count,approved=True,username=username)
    if new:
      mailto = getattr(settings,"INSTAGRAM_EMAIL",settings.ADMINS)
      print "emailing %s to %s"%(new,mailto)
      send_mail(
        "New Instagram Photos",
        "There are %s new instagram photos. Pleas visit the admin to approve them."%new,
        "noreply@txrxlabs.org",
        mailto,
        )
