from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Photo, PhotoTag
from .forms import PhotoForm, PhotoFilterForm, ZipForm, PhotoTagForm

from NextPlease import pagination

@staff_member_required
@pagination('photos',per_page=12,orphans=5)
def insert_photo(request):
  photos = Photo.objects.all()
  if request.GET.get('mine',False):
    photos = photos.filter(user=request.user)
  form = PhotoFilterForm(request.GET or None,initial={'mine':True})
  query = request.GET.get('search','')
  if query:
    _q = Q(caption__icontains=query)
    _q = _q | Q(filename__icontains=query)
    _q = _q | Q(name__icontains=query)
    photos = photos.filter(_q).distinct()
  values = {
    "photos": photos,
    "form": form,
  }
  return TemplateResponse(request,"photo/insert_photo.html",values)

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
  return TemplateResponse(request,"photo/add_photo.html",values)

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

@staff_member_required
def bulk_tag_index(request):
  phototags = PhotoTag.objects.all()
  form = PhotoTagForm(request.POST or None)
  if form.is_valid():
    phototag = form.save()
    messages.success(request,"New PhotoTag created: %s"%phototag)
    return HttpResponseRedirect(request.get_full_path())
  values = {'phototags': phototags,'form': form}
  return TemplateResponse(request,"photo/bulk_tag_index.html",values)

@csrf_exempt
@staff_member_required
@pagination('photos',per_page=96,orphans=5)
def bulk_tag_detail(request,tag_id):
  phototag = PhotoTag.objects.get(pk=tag_id)
  if request.POST:
    photo = Photo.objects.get(pk=request.POST['photo_pk'])
    if request.POST['checked'] == 'true':
      photo.tags.add(phototag)
    else:
      photo.tags.remove(phototag)
    photo.save()
    return HttpResponse('{success:true}')
  values = {
    'phototag': phototag,
    'photos': Photo.objects.all()
  }
  return TemplateResponse(request,"photo/bulk_tag_detail.html",values)
