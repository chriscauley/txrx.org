from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect

redirect = lambda request,url: HttpResponseRedirect(url)
predirect = lambda request,url: HttpResponsePermanentRedirect(url)



