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

def photoset_from_zip(path,approved=True):
    """turn a zip file into a photoset"""
    now = datetime.datetime.now()
    _ = now.strftime(Photo._meta.get_field('file').upload_to)
    zip_name = path.split('/')[-1]
    root = os.path.join(settings.MEDIA_ROOT,_)
    if not os.path.exists(root):
        os.mkdir(root)
    directory = os.path.join(root,'%s_%s'%(now.day,now.time()))
    os.mkdir(directory)
    new_path = os.path.join(directory,zip_name)
    os.chdir(directory)
    os.rename(path,new_path)
    command = 'unzip %s'%new_path
    process = Popen(command, stdout=PIPE, shell=True)
    process.communicate()
    for folder,_,files in os.walk('.'):
        for f in files:
            print folder, f
            os.rename(os.path.join(folder,f),os.path.join(directory,f))
    photoset,new = PhotoSet.objects.get_or_create(
        title = 'uploaded photos: %s'%zip_name,
        user_id=1,
        )
    folders = [f for f in os.listdir(directory) if os.path.isdir(f)]
    for f in folders:
        os.rmdir(f)
    files = [f for f in os.listdir(directory) if not os.path.isdir(f)]
    for f_path in files:
        print "creating photo!"
        photo = Photo(
            file = os.path.join(directory,f_path),
            source = "misc",
            approved = approved,
            )
        photo.save()
        SetPhoto(photo=photo,photoset=photoset).save()
    #all done, delete the zip!
    os.remove(new_path)

z = photoset_from_zip
