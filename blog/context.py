from django.conf import settings


def process(request):
    contexts = {}

    # add SITE_TAGLINE, and SITE_NAME, and VERSION to the context
    contexts.update({'SITE_TAGLINE': settings.SITE_TAGLINE})
    contexts.update({'SITE_NAME': settings.SITE_NAME})
    contexts.update({'VERSION': settings.VERSION})
    contexts.update({'ANALYTICS_CODE': settings.ANALYTICS_CODE})
    contexts.update({'SITE_URL': settings.SITE_URL})

    return contexts
