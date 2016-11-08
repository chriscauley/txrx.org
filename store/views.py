from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Consumable
from course.models import CourseEnrollment
from user.models import is_shopkeeper, is_toolmaster

from drop.models import Order, Category
from drop.util.cart import get_or_create_cart

import json, datetime

def categories_json(request):
  return JsonResponse({'categories': [c.as_json for c in Category.objects.all()]})

@login_required
def index(request):
  cart = json.dumps({ci.product_id: ci.quantity for ci in get_or_create_cart(request).items.all()})
  values = {
    'cart': cart
  }
  return TemplateResponse(request,'store/index.html',values)

def start_checkout(request):
  cart = get_or_create_cart(request,save=True)
  cart.update(request)
  try:
    order = Order.objects.filter(cart_pk=cart.pk,status__lt=Order.PAID)[0]
  except IndexError:
    order = Order.objects.create_from_cart(cart,request)
  order.status = Order.CONFIRMED
  order.save()
  out = {
    'order_pk': order.pk,
    '_errors': []
  }
  for item in cart.items.all():
    if item.product.in_stock is None:
      continue
    if item.product.in_stock < item.quantity:
      s = "Sorry, we only have %s in stock of the following item: %s"
      out['_errors'].append(s%(item.product.in_stock,item.product))
  return HttpResponse(json.dumps(out))

@user_passes_test(is_toolmaster)
@csrf_exempt
def checkouts(request):
  if request.POST:
    courseenrollment = CourseEnrollment.objects.get(pk=request.POST['pk'])
    courseenrollment.completed = courseenrollment.failed = None
    action = request.POST.get('action',None).lower()
    status = "neither"
    if action == "pass":
      courseenrollment.completed = datetime.datetime.now()
      status = "passed"
    if action == "fail":
      courseenrollment.failed = datetime.datetime.now()
      status = "failed"
    courseenrollment.save()
    messages.success(request,"%s marked as %s."%(courseenrollment,status))
    return HttpResponseRedirect('.')
  cutoff = datetime.datetime.now()-datetime.timedelta(60)
  base_enrollments = CourseEnrollment.objects.filter(datetime__gte=cutoff)
  incomplete = base_enrollments.filter(completed=None,failed=None).order_by("-datetime")
  failed = base_enrollments.filter(failed__isnull=False).order_by("-failed")
  complete = base_enrollments.filter(completed__isnull=False).order_by("-completed")
  values = {
    'incomplete_enrollments': incomplete,
    'completed_enrollments': complete,
    'failed_enrollments': failed,
  }
  return TemplateResponse(request,'store/checkouts.html',values)

@user_passes_test(is_shopkeeper)
@csrf_exempt
def receipts(request):
  if request.POST:
    o = Order.objects.get(pk=request.POST['pk'])
    o.status = int(request.POST['status'])
    o.save()
    now = datetime.datetime.now().strftime("%m/%d/%Y at %H:%M")
    status = "delivered" if o.status == Order.SHIPPED else "outstanding"
    t = "%s marked as %s on %s"%(request.user,status,now)
    messages.success(request,"%s marked as %s"%(o,status))
    o.extra_info.create(text=t)
    return HttpResponseRedirect('.')
  values = {
    'order_sets': [
      ["Outstanding Orders", Order.objects.filter(status=Order.PAID).order_by("-id")],
      ["Delivered Orders", Order.objects.filter(status=Order.SHIPPED).order_by("-id")[:10]],
    ]
  }
  return TemplateResponse(request,'store/receipts.html',values)

@user_passes_test(is_shopkeeper)
@csrf_exempt
def admin_page(request):
  values = {}
  return TemplateResponse(request,'store/admin.html',values)

@user_passes_test(is_shopkeeper)
def admin_products_json(request):
  extra_fields = ['purchase_url','purchase_domain','purchase_url2','purchase_domain2',
                  'purchase_quantity','in_stock']
  out = {product.pk:{k:getattr(product,k) for k in extra_fields}
         for product in Consumable.objects.filter(active=True)}
  return HttpResponse("window.PRODUCTS_EXTRA = %s;"%json.dumps(out))

@user_passes_test(is_shopkeeper)
@csrf_exempt
def admin_add(request):
  quantity = int(request.POST['quantity'])
  product = get_object_or_404(Consumable,pk=request.POST['pk'])
  old = product.in_stock or 0 
  product.in_stock = max(old + quantity,0)
  product.save()
  return HttpResponse(str(product.in_stock))
