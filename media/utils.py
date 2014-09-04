from django.conf import settings
import os, datetime

from subprocess import Popen, PIPE

from models import Photo

def photos_from_zip(path,approved=True,user=None):
    """turn a zip file into a photos"""
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
            os.rename(os.path.join(folder,f),os.path.join(directory,f))
    folders = [f for f in os.listdir(directory) if os.path.isdir(f)]
    for f in folders:
        os.rmdir(f)
    files = [f for f in os.listdir(directory) if not os.path.isdir(f)]
    for f_path in files:
        print "creating photo!"
        photo = Photo(
            file = os.path.join(directory,f_path).split(settings.MEDIA_ROOT)[-1],
            source = "misc",
            approved = approved,
            user=user
            )
        photo.save()
    #all done, delete the zip!
    os.remove(new_path)
