from django.conf import settings

def process(request):
  return {
    'STATIC_URL': settings.STATIC_URL,
    }
