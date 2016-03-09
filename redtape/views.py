from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import Document, Signature
from .forms import SignatureForm

from collections import defaultdict
from lablackey.utils import get_or_none
import json

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

def documents_json(request):
  documents = Document.objects.all()
  return HttpResponse(json.dumps([d.as_json for d in documents]))

@staff_member_required
def aggregate(request,document_pk):
  document = get_object_or_404(Document,pk=document_pk)
  others = defaultdict(lambda: [])
  results = defaultdict(lambda:0)
  for s in document.signature_set.all():
    s_json = json.loads(s.data)
    key = s_json['how-did-you-hear-about-us']
    if not key:
      continue
    results[key] += 1
    if s_json['other']:
      others[key].append(s_json['other'].title())

  values = {
    'results': sorted(results.items(),key=lambda t:t[1],reverse=True),
    'others': [(key,sorted(rs)) for key,rs in sorted(others.items())]
  }
  return TemplateResponse(request,"redtape/aggregate.html",values)
