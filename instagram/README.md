Django Instagram
========

Quick Start
--------

Add instagram to the INSTALLED_APPS variable in your settings.py

```python
INSTALLED_APPS = (
  ...
  'instagram',
)
```

Next create the instagram tables in the database using `syncdb` or (if you are using south for migrations) `migrate`:

```bash
python manage.py syncdb
python manage.py migrate
```

At very minimum, you will need a unique `INSTAGRAM_TOKEN` setting and an `INSTAGRAM_TAG`, `INSTAGRAM_USERNAME`, or `INSTAGRAM_USERID`. Without an `INSTAGRAM_TOKEN` you cannot access the API. Without one of the other three settings to follow `python manage.py update_instagram` does nothing (since you haven't specified anything to follow). This app was built using the following tag:

```python
INSTAGRAM_TAG = "txrx"
```

Finally, run `python manage.py update_instagram` to pull the latest photos from instagram. Any new, unapproved photos will generate an email alerting. Photos will not be displayed on the site if they are not approved.

Approve photos at `http://yourdomain.com/admin/instagram/instagramphoto/`.

If you want to use the built in template and view, add the following to your main `urls.py` file:

```python
urlpatterns = patterns(
  '',
  url(r'^instagram/',include('instagram.urls')),
)
```

You can now view all instagram photos at `http://yourdomain.com/instagram/`.


Settings
--------

INSTAGRAM_TOKEN - (str) Your secret key from instagram.

INSTAGRAM_TAG - (str) An instagram tag you want to follow. 

INSTAGRAM_USERNAME - (str) An instagram username that you want to follow. If you specify an `INSTAGRAM_USERID`, then this setting does nothing when you run `python manage.py update_instagram`.

INSTAGRAM_USERID - (int) An instagram user id to follow.

INSTAGRAM_EMAIL - (str) An email address that you want to be alerted when new photos arrive that need to be approved. If empty this will email the ADMINS variable in settings.

APPROVE_INSTAGRAM - (bool, default=`False`) Whether or not all new photos should be automatically approved. Recommended as False, unless you are following a user that is trusted.

INSTAGRAM_DIR - (str, default=`'uploads/instagram'`) The directory to save photos to, which is the `upload_to` argument on all `models.ImageField` fields. If this is not an absolute path, django automatically uses `settings.MEDIA_ROOT` as the root. 


Models
--------

`instagram.models.InstagramPhoto` - The main model containing all data around a photo, incluing all three photo sizes. See http://instagram.com/developer/endpoints/media/

These models are "followables", meaning that they have a boolean for "follow" and "approved". If you mark the instance as "follow" then `python manage.py update_instagram` will check instagram for new photos associated with the model. If you mark an instance as "approved", then all the photos downloaded with the management command will be automatically approved (mostly used for trusted users).

`instagram.models.InstagramLocation` - The location the photo was taken at. See http://instagram.com/developer/endpoints/locations/

`instagram.models.InstagramUser` - An instagram user which can be associated with a `django.contrib.auth.models.User`. See http://instagram.com/developer/endpoints/users/

`instagram.models.InstagramTag` - An instagram hash tag. If a photos comment contains '#hashtag', it will be saved with the tag 'hashtag' (without the pound sign). See http://instagram.com/developer/endpoints/tags/
