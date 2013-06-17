from datetime import datetime
from timezones.utils import adjust_datetime_to_timezone
from django.conf import settings
import os, datetime

from subprocess import Popen, PIPE

from models import Photo, PhotoSet, SetPhoto

def localize_date(date, from_tz=None, to_tz=None):
    """
    Convert from one timezone to another
    """
    # set the defaults
    if from_tz is None:
        from_tz = settings.TIME_ZONE

    if to_tz is None:
        to_tz = "US/Central"

    date = adjust_datetime_to_timezone(date, from_tz=from_tz, to_tz=to_tz)
    date = date.replace(tzinfo=None)
    return date

def photoset_from_zip(path):
    """turn a zip file into a photoset"""
    now = datetime.datetime.now()
    _ = now.strftime(Photo._meta.get_field('file').upload_to)
    zip_name = path.split('/')[-1]
    root = os.path.join(settings.MEDIA_URL,_)
    if not os.path.exists(root):
        os.mkdir(root)
    directory = os.path.join(root,'%s_%s'%(now.day,now.time()))
    os.mkdir(directory)
    os.chdir(directory)
    command = 'unzip %s'%path
    process = Popen(command, stdout=PIPE, shell=True)
    files = os.listdir(directory)
    photoset = PhotoSet(
        title = 'uploaded photos: %s'%zip_name,
        user_id=1,
        )
    photoset.save()
    for f_path in files:
        photo = Photo(
            file = os.path.join(directory,f_path),
            source = "misc",
            )
        photo.save()
        SetPhoto(photo=photo,photoset=photoset).save()
    
