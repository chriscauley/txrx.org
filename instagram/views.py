from django.template.response import TemplateResponse
from django.core.paginator import EmptyPage, Paginator
from django.http import Http404
from .models import InstagramPhoto

def index(request):
  photos = InstagramPhoto.objects.filter(approved=True)
  paginator = Paginator(photos,6)
  page_number = request.GET.get('page',1)
  try:
    page = paginator.page(page_number)
  except EmptyPage:
    raise Http404
  values = {
    'paginator': paginator,
    'page': page
    }
  return TemplateResponse(request,'instagram/index.html',values)
