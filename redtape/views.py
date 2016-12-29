from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.static import serve

from .models import Document, Signature, UploadedFile
from .forms import SignatureForm
from membership.utils import temp_user_required

from collections import defaultdict
from lablackey.utils import get_or_none
from lablackey.mail import send_template_email
import json

#! TODO Possibly depracated 12/2016
def document_detail(request,document_pk,slug=None): #ze slug does notzing!
  document = get_object_or_404(Document,pk=document_pk)
  if document.login_required and not request.user.is_authenticated():
    return login_required(document_detail)(request,document_pk)
  signature = None
  if request.user.is_authenticated() and document.editable:
    signature = get_or_none(Signature,document_id=document_pk,user=request.user)
  form = SignatureForm(request.POST or None,request.FILES or None,document=document,instance=signature)
  if form.is_valid():
    signature = form.save(commit=False)
    if request.user.is_authenticated():
      signature.user = request.user
    signature.save()
    messages.success(request,"%s signed by %s"%(document,signature.user))
    return HttpResponseRedirect(request.POST.get('next',""))
  values = {
    'form': form,
    'document': document,
    'signature': signature
  }
  return TemplateResponse(request,"redtape/document.html",values)

@temp_user_required
def document_json(request,document_pk):
  #! TODO do we want to allow annonymous documents?
  document = get_object_or_404(Document,pk=document_pk)
  signature = None
  if document.editable:
    signature = get_or_none(Signature,document_id=document_pk,user=request.temp_user)
  form = SignatureForm(request.POST or None,request.FILES or None,document=document,instance=signature)
  if form.is_valid():
    signature = form.save(commit=False)
    if request.temp_user.is_authenticated():
      signature.user = request.temp_user
    signature.save()
    m = "%s signed by %s"%(document,signature.user)
    document_json = document.get_json_for_user(request.temp_user)
    #signature.delete() #! TODO this is only to help debugging!
    return JsonResponse({"messages":[{"level": 'success','body': m}], 'document': document_json})
  out = "Please correct the following error(s):"
  for i in form.errors.items():
    out += "<br/>%s: %s"%i
  return JsonResponse({'errors': {'non_field_error': out}})

def post_document(request,pk):
  document = get_object_or_404(Document,pk=pk)
  signature = Signature(document=document)
  signature.data = json.dumps({ f.get_name(): request.POST.get(f.get_name(),None) for f in document.documentfield_set.all() })
  if request.user.is_authenticated():
    signature.user = request.user
  signature.save()
  if document.pk == 5: #this will probably need to be abstracted at some point
    send_template_email("email/work_request",['work@txrxlabs.org'],context={'signature':signature})
  return JsonResponse({"ur_alert_success": "%s has been saved."%document.name})

@login_required
def index(request):
  d_ids = getattr(settings,"REQUIRED_DOCUMENT_IDS",[])
  documents = Document.objects.filter(id__in=d_ids)
  values = {
    'documents_signatures': [(d,get_or_none(Signature,document_id=d.id,user=request.user)) for d in documents],
    'next': request.path,
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

def post_file(request):
  f = request.FILES['file']
  obj = UploadedFile(
    src = f,
    name = f.name,
    content_type=f.content_type,
  )
  obj.save()
  return JsonResponse(obj.as_json)

@login_required
def private_file(request,slug):
  f = get_object_or_404(UploadedFile,src=slug)
  if not request.user.is_staff and f.user != request.user:
    return HttpResponse("Not Allowed - Only the staff and the person who uploaded this file can view it.",status=403)
  return serve(request, f.src.path.split(settings.PRIVATE_ROOT)[-1], settings.PRIVATE_ROOT)
