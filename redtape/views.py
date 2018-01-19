from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import Document, Signature
from .forms import SignatureForm
from membership.utils import temp_user_required

from collections import defaultdict
from lablackey.utils import get_or_none
from lablackey.mail import send_template_email, render_template
from freshdesk.api import API
import json

@temp_user_required
def document_json(request,document_pk):
  #! TODO do we want to allow annonymous documents?
  document = get_object_or_404(Document,pk=document_pk)
  signature = None
  if document.editable:
    signature = get_or_none(Signature,document_id=document_pk,user=request.temp_user)
  form = SignatureForm(request,document=document,instance=signature)
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
  signature.data = { f.get_name(): request.POST.get(f.get_name(),None) for f in document.documentfield_set.all() }
  if request.user.is_authenticated():
    signature.user = request.user
  signature.save()
  if document.pk == 5: #! TODO this will probably need to be abstracted at some point
    a = API("txrxlabs.freshdesk.com",settings.FRESHDESK_API_KEY,version=2)
    error = None
    try:
      send_template_email("email/work_request",['roland.von.k@txrxlabs.org'],context={'signature':signature,"error":error})
      a.tickets.create_ticket('New work request for %s'%signature.data['name'],
                              email=signature.data['email'],
                              description=render_template("email/work_request",{'signature':signature})[0],
                              tags=['work'])
    except Exception,e:
      error = e
    send_template_email("email/work_request",['chris@lablackey.com'],context={'signature':signature,"error":error})
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
    key = s.data['how-did-you-hear-about-us']
    if not key:
      continue
    results[key] += 1
    if s.data['other']:
      others[key].append(s.data['other'].title())

  values = {
    'results': sorted(results.items(),key=lambda t:t[1],reverse=True),
    'others': [(key,sorted(rs)) for key,rs in sorted(others.items())]
  }
  return TemplateResponse(request,"redtape/aggregate.html",values)
