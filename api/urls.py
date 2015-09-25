from django.conf.urls import url, patterns
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import RequestFactory

request_factory = RequestFactory()
from .serializers import BaseSizzler

def import_serializers(app_label):
  try:
    app_serializers = __import__(app_label+".serializers",fromlist=['serializers'])
  except ImportError:
    return []

  #! TODO
  #really this next line should be isinstance of a custom class
  #autosizzler should also be of that class
  return [(name, cls) for name, cls in app_serializers.__dict__.items() if name.endswith("Sizzler")]

def auto_serializer(model, modeladmin):
  request = request_factory.get('/')
  request.user = get_user_model()(is_superuser=True)

  class AutoSizzler(BaseSizzler):
    class Meta:
      pass
  AutoSizzler.Meta.model = model
  fields = list(modeladmin.get_fields(request))
  #if not model._meta.pk.name in fields:
  #  fields.append(model._meta.pk.name)
  #AutoSizzler.Meta.fields = fields
  return AutoSizzler

def build_urls():
  # This will do for now since I really need to get back to TXRX programming
  #! TODO This should be split into build_map and build_urls
  #! TODO look into how admin register goes and do it here too.
  app_map = {}
  out = []
  for model, modeladmin in admin.site._registry.items():
    app_label = model._meta.app_label
    model_name = model.__name__
    app_map[app_label] = app_map.get(app_label,{})

  for app_label,app_dict in app_map.items():
    for name,serializer in import_serializers(app_label):
      print name
      url_name = name.lower()
      if url_name.endswith("sizzler"):
        url_name = url_name[:-7] # len("sizzler")
      app_map[app_label][url_name] = serializer

  for model, modeladmin in admin.site._registry.items():
    app_label = model._meta.app_label
    model_name = model.__name__
    if not model_name.lower() in app_map[app_label]:
      app_map[app_label][model_name.lower()] = auto_serializer(model,modeladmin)
    serializer = app_map[app_label][model_name.lower()]

  for app_label, d in app_map.items():
    for s_name, serializer in d.items():
      kwargs = {'serializer': serializer}
      _url = u'^(%s)/(%s)/'%(app_label,s_name)
      out.append(url(_url+"$",'list_view',name="api_list_view",kwargs=kwargs))
      out.append(url(_url+"(\d+)/$",'detail_view',name="api_list_view",kwargs=kwargs))
  return out

urlpatterns = patterns(
  'api.views',
  *build_urls()
)
