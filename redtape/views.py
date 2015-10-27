from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import Document
from .forms import SignatureForm

def document_detail(request,document_pk):
  document = get_object_or_404(Document,pk=document_pk)
  if document.login_required and not request.user.is_authenticated():
    return login_required(document_detail)(request,document_pk)
  form = SignatureForm(request.POST or None,request.FILES or None,initial={'document':document})
  if form.is_valid():
    signature = form.save(commit=False)
    if request.user.is_authenticated():
      signature.user = request.user
    signature.save()
    messages.success(request,"%s signed by %s"%(document,signature.name_typed))
    return HttpResponseRedirect('')
  values = {
    'form': form,
    'document': document,
  }
  return TemplateResponse(request,"redtape/document.html",values)
