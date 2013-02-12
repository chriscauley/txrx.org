from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime, requests, simplejson, os, re

photofile_path = getattr(settings,"INSTAGRAM_DIR",'uploads/instagram')

class FollowableModel(models.Model):
  follow = models.BooleanField(default=False,help_text="Searches for photos belonging to this when update_instagram is run")
  approved = models.BooleanField(default=False,help_text="Automatically mark all photos of this type as approved, user with caution")
  token = getattr(settings,"INSTAGRAM_TOKEN")
  @property
  def latest_url(self):
    return self.feed_url%(self.feed_param,self.token)
  def follow_me(self):
    request = requests.get(self.latest_url)
    json = simplejson.loads(request.text)
    save_photos(json,approved=self.approved)
  class Meta:
    abstract = True

class InstagramUserManager(models.Manager):
  def get_or_create_from_username(self,username=None):
    try:
      return self.get(username=username), False
    except self.model.DoesNotExist:
      obj = self.model(username=username)
      obj.update_and_save()
      return obj, True

class InstagramUser(FollowableModel):
  iid = models.CharField(max_length=32) #instagram id!
  username = models.CharField(max_length=128,null=True,blank=True)
  profile_picture = models.ImageField(upload_to=photofile_path,null=True,blank=True)
  full_name = models.CharField(max_length=128,null=True,blank=True)
  bio = models.TextField(null=True,blank=True)
  website = models.URLField(verify_exists=False,null=True,blank=True)
  user = models.ForeignKey(User,null=True,blank=True)

  feed_url = "https://api.instagram.com/v1/users/search?q=%s&access_token=%s"
  feed_param = property(lambda self: self.iid)
  __unicode__ = lambda self: self.username
  objects = InstagramUserManager()

  def update_and_save(self):
    url = "https://api.instagram.com/v1/users/search?q=%s&access_token=%s"%(self.username,self.token)
    json = simplejson.loads(requests.get(url).text)
    for user in json['data']:
      if user['username'] == self.username:
        self.iid = user['id']
        self.save()
        return

class InstagramTag(FollowableModel):
  name = models.CharField(max_length=128)

  feed_url = "https://api.instagram.com/v1/tags/%s/media/recent?access_token=%s"
  feed_param = property(lambda self: self.name)
  __unicode__ = lambda self: self.name

class InstagramLocationManager(models.Manager):
  def get_from_json(self,json):
    if not json: #some just don't have locations!
      return 
    if 'id' in json:
      location,new = InstagramLocation.objects.get_or_create(iid=json.pop('id'),defaults=json)
      if new:
        print "New Location: %s"%location
      return location

    # search instagram for any APPROVED locations nearby that are already in the database
    r = requests.get(self.model.search_url%(json['latitude'],json['longitude'],self.model.token))
    response = simplejson.loads(r.text)
    for l in response['data']:
      try:
        return InstagramLocation.objects.get(iid=l['id'],approved=True)
      except InstagramLocation.DoesNotExist:
        pass
    
class InstagramLocation(FollowableModel):
  name = models.CharField(max_length=128)
  latitude = models.FloatField()
  longitude = models.FloatField()
  iid = models.CharField(max_length=32) #instagram id!

  feed_url = "https://api.instagram.com/v1/locations/%s?access_token=%s"
  feed_param = lambda self: self.iid
  search_url = "https://api.instagram.com/v1/locations/search?lat=%s&lng=%s&access_token=%s"
  objects = InstagramLocationManager()
  __unicode__ = lambda self: "Instagram Location: %s"%self.name

class InstagramPhoto(models.Model):
  thumbnail = models.ImageField(upload_to=photofile_path,null=True,blank=True)
  low_resolution = models.ImageField(upload_to=photofile_path,null=True,blank=True)
  standard_resolution = models.ImageField(upload_to=photofile_path,null=True,blank=True)

  instagram_user = models.ForeignKey(InstagramUser,null=True,blank=True)
  instagram_location = models.ForeignKey(InstagramLocation,null=True,blank=True)
  instagram_tags = models.ManyToManyField(InstagramTag,null=True,blank=True)

  caption = models.CharField(max_length=255,null=True,blank=True)
  created_time = models.IntegerField()
  iid = models.CharField(max_length=32) #instagram id!
  approved = models.BooleanField(default=False)
  rejected = models.BooleanField(default=False)

  __unicode__ = lambda self: "Instagram Photo by %s"%(self.username)
  thumbnail_ = lambda self: '<img src="%s" height="75" />'%self.thumbnail.url
  thumbnail_.allow_tags=True
  @property
  def name(self):
    return "Instagram Photo by: %s"%self.username
  @property
  def datetime(self):
    return datetime.datetime.utcfromtimestamp(float(self.created_time))
  class Meta:
    ordering = ("-created_time",)

def save_photos(response,approved=False,username=""):
  photo_dir = os.path.join(settings.MEDIA_ROOT,photofile_path)
  if not os.path.exists(photo_dir):
    os.mkdir(photo_dir)
  for item in response['data']: # image dicts
    defaults = dict(
      created_time = item['created_time'],
      approved = approved,
      )
    if item['caption']:
      username = item['caption']['from']['username']
      defaults['caption'] = item['caption']['text']
    if username:
      user,new = InstagramUser.objects.get_or_create_from_username(username=username)
      defaults['instagram_user'] = user
    i,new = InstagramPhoto.objects.get_or_create(iid=item['id'],defaults=defaults)
    if new: # save photos
      tags = re.findall('#([\w\d]+)',i.caption or '')
      for tag_name in tags:
        tag, new = InstagramTag.objects.get_or_create(name=tag_name)
        i.instagram_tags.add(tag)
        
      i.location = InstagramLocation.objects.get_from_json(item['location'])
      i.save()
      for size in ['thumbnail','low_resolution','standard_resolution']:
        url = item['images'][size]['url']
        ri = requests.get(url,stream=True)
        path = os.path.join(photo_dir,url.split("/")[-1])
        f = open(path,'w')
        f.write(ri.raw.read())
        f.close()
        setattr(i,size,path.split('media/')[-1])
        i.save()

