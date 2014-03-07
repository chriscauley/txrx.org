"""Main codrspace views"""
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from codrspace.models import Photo
from codrspace.forms import PhotoForm, PhotoFilterForm, ZipForm

from NextPlease import pagination

@staff_member_required
def insert_photo(request):
  photos = Photo.objects.all()
  if not request.GET or request.GET.get('mine',False):
    photos = photos.filter(user=request.user)
  form = PhotoFilterForm(request.GET or None,initial={'mine':True})
  paginator = None
  if photos:
    paginator = Paginator(photos,8)
    photos = paginator.page(request.GET.get('page',1))
  values = {
    "paginator": paginator,
    "photos": photos,
    "form": form,
    }
  return TemplateResponse(request,"codrspace/insert_photo.html",values)

@staff_member_required
def add_photo(request):
  photo = None
  form = PhotoForm(request.POST or None,request.FILES or None)
  if request.POST and form.is_valid():
    photo = form.save()
    photo.user = request.user
    photo.save()
    # Not redirecting because we're going to close modal using javascript
  values = {
    'photo': photo,
    'form': form,
    }
  return TemplateResponse(request,"codrspace/add_photo.html",values)

@staff_member_required
def upload_zip(request):
  form = ZipForm(request.POST or None, request.FILES or None)
  if request.POST and form.is_valid():
    z = request.FILES['zip_file']
    folder = os.path.join(settings.MEDIA_ROOT,'zip_temp')
    if not os.path.exists(folder):
      os.mkdir(folder)
    folder = os.path.join(folder,z.name)
    os.mkdir(folder)
    with open('tmp', 'wb+') as destination:
      for chunk in f.chunks():
        destination.write(request.FILES['zip_file'])
