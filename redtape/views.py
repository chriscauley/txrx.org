from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import Document
from .forms import SignatureForm

import json

def document_detail(request,document_pk,slug=None): #ze slug does notzing!
  document = get_object_or_404(Document,pk=document_pk)
  if document.login_required and not request.user.is_authenticated():
    return login_required(document_detail)(request,document_pk)
  form = SignatureForm(request.POST or None,request.FILES or None,document=document)
  if form.is_valid():
    signature = form.save(commit=False)
    if request.user.is_authenticated():
      signature.user = request.user
    signature.save()
    messages.success(request,"%s signed by %s"%(document,signature.name_typed or signature.user))
    return HttpResponseRedirect('')
  values = {
    'form': form,
    'document': document,
  }
  return TemplateResponse(request,"redtape/document.html",values)

def documents_json(request):
  documents = Document.objects.all()
  return HttpResponse(json.dumps([d.as_json for d in documents]))
