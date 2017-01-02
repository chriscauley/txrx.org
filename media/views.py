from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

from .models import Photo, PhotoTag, TaggedPhoto, UploadedFile
from .forms import PhotoForm, PhotoFilterForm, ZipForm, PhotoTagForm

from NextPlease import pagination
from PIL import Image

import json

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
  phototag = PhotoTag.objects.get(id=tag_id)
  if request.POST:
    photo = Photo.objects.get(id=request.POST['photo_id'])
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

@staff_member_required
def photo_search(request):
  q = request.GET['q']
  photos = Photo.objects.filter(Q(name__icontains=q)|Q(caption__icontains=q))
  return HttpResponse(json.dumps([p.as_json for p in photos]))

@staff_member_required
def tag_photo(request):
  natural_key = request.GET.get('content_type').split('.')
  content_type = ContentType.objects.get_by_natural_key(*natural_key)
  photo = Photo.objects.get(id=request.GET['photo_id'])
  tag,new = TaggedPhoto.objects.get_or_create(
    photo=photo,
    object_id=request.GET['object_id'],
    content_type=content_type,
  )
  return HttpResponse(json.dumps(new))

@staff_member_required
def bulk_photo_upload(request):
  image_list = []
  if request.method == "POST" and request.FILES:
    natural_key = request.POST.get('content_type').split('.')
    content_type = ContentType.objects.get_by_natural_key(*natural_key)
    for f in request.FILES.getlist('file'):
      try:
        Image.open(f)
      except IOError:
        image_list.append({
          'error':"This does not appear to be a valid image",
          'name': f.name
        })
        continue
      photo = Photo.objects.create(
        file=f,
        user=request.user
      )
      image_list.append(photo.as_json)
      TaggedPhoto.objects.create(
        photo=photo,
        object_id=request.POST['object_id'],
        content_type=content_type,
      )
  return HttpResponse(json.dumps(image_list))

@csrf_exempt
@staff_member_required
def untag_photo(request):
  natural_key = request.POST.get('content_type').split('.')
  content_type = ContentType.objects.get_by_natural_key(*natural_key)
  TaggedPhoto.objects.filter(content_type=content_type,
                          object_id=request.POST['object_id'],
                          photo__id=request.POST['photo_id']).delete()
  return HttpResponse('')

@csrf_exempt
@staff_member_required
def delete_photo(request,pk):
  Photo.objects.filter(pk=pk).delete()
  return HttpResponse('')

@csrf_exempt
@staff_member_required
def edit_photo(request,pk):
  photo = Photo.objects.get(pk=pk)
  photo.name = request.POST['name'].replace('\n','').strip()
  photo.save()
  return HttpResponse('')

def post_file(request):
  f = request.FILES['file']
  obj = UploadedFile(
    src = f,
    name = f.name,
    content_type=f.content_type,
  )
  obj.save()
  return JsonResponse(obj.as_json)

@login_required
def private_file(request,slug):
  f = get_object_or_404(UploadedFile,src=slug)
  if not request.user.is_staff and f.user != request.user:
    return HttpResponse("Not Allowed - Only the staff and the person who uploaded this file can view it.",status=403)
  return serve(request, f.src.path.split(settings.PRIVATE_ROOT)[-1], settings.PRIVATE_ROOT)
