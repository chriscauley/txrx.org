from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import Document, Signature
from .forms import SignatureForm

from lablackey.utils import get_or_none

def document_detail(request,document_pk,slug=None): #ze slug does notzing!
  document = get_object_or_404(Document,pk=document_pk)
  if document.login_required and not request.user.is_authenticated():
    return login_required(document_detail)(request,document_pk)
  instance = None
  if request.user.is_authenticated():
    instance = get_or_none(Signature,document_id=document_pk,user=request.user)
  form = SignatureForm(request.POST or None,request.FILES or None,document=document,instance=instance)
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

@login_required
def index(request):
  d_ids = getattr(settings,"REQUIRED_DOCUMENT_IDS",[])
  documents = Document.objects.filter(id__in=d_ids)
  values = {
    'documents_signatures': [(d,get_or_none(Signature,document_id=d.id,user=request.user)) for d in documents],
  }
  return TemplateResponse(request,"redtape/index.html",values)
