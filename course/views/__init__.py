from django.contrib.auth import get_user_model
from django.http import QueryDict, Http404, HttpResponseRedirect
from django.template.response import TemplateResponse

from ..models import Session
from db.utils import get_or_none

from paypal.standard.ipn.models import *

def debug_parsing(request, id):
  ipn = PayPalIPN.objects.get(id=id)

  query = ipn.query
  #add them to the classes they're enrolled in
  params = QueryDict(ipn.query)
  class_count = int(params['num_cart_items'])
  course_info = []

  for i in range(1, class_count+1):
    session_id = int(params['item_number%d' % (i, )])
    section_cost = int(float(params['mc_gross_%d' % (i, )]))
    session = Session.objects.get(id=session_id)
    course_info.append((session_id, section_cost))

    return TemplateResponse(request,"course/debug.html",locals())

def paypal_return(request):
  User = get_user_model()
  session_ids = [v for k,v in request.REQUEST.items() if k.startswith('item_number')]
  if not ('payer_email' in request.REQUEST) or not session_ids:
    raise Http404
  email = request.REQUEST['payer_email']
  sessions = Session.objects.filter(pk__in=session_ids)
  matched_user = None
  if not request.user.is_authenticated():
    matched_user = get_or_none(User,email=email)
    matched_user = matched_user or get_or_none(User,usermembership__paypal_email=email)
  values = {
    'email': email,
    'sessions': sessions,
    'matched_user': matched_user,
  }
  return TemplateResponse(request,"course/paypal_return.html",values)
