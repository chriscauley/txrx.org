from django.template.response import TemplateResponse

from .models import Category, Consumable

def index(request):
  consumables = Consumable.objects.filter(active=True)
  values = {
    'consumables': consumables,
  }
  return TemplateResponse(request,'store/index.html',values)
