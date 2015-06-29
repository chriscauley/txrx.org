from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Category, reset_products_json

from shop.models import Product, CartItem, Order
from shop.util.cart import get_or_create_cart

import json;

def index(request):
  cart = json.dumps({ci.product_id: ci.quantity for ci in get_or_create_cart(request).items.all()})
  values = {
    'cart': cart
  }
  return TemplateResponse(request,'store/index.html',values)

def products_json(request):
  return HttpResponse(reset_products_json())

def detail(request,pk,slug):
  product = get_object_or_404(Product,pk=pk)
  values = {
    'product': product,
  }
  return TemplateResponse(request,'store/detail.html',values)

@csrf_exempt
def cart_edit(request):
  cart = get_or_create_cart(request,save=True)
  quantity =  int(request.POST['quantity'])
  product = Product.objects.get(pk=request.POST['pk'])
  defaults = {'quantity': 0}
  cart_item,new = CartItem.objects.get_or_create(product=product,cart=cart,defaults=defaults)
  if new:
    print "created!"
  print cart_item.quantity
  if quantity:
    cart_item.quantity = quantity
    cart_item.save()
  else:
    cart_item.delete()
    print "deleted"

  cart.update(request)
  return HttpResponse('')

def start_checkout(request):
  cart = get_or_create_cart(request,save=True)
  cart.update(request)
  order = Order.objects.create_from_cart(cart,request)
  order.status = Order.COMPLETED
  order.save()
  return HttpResponse(str(order.pk))

@staff_member_required
@csrf_exempt
def receipts(request):
  if request.POST:
    o = Order.objects.get(pk=request.POST['pk'])
    o.status = request.POST['status']
    o.save()
    return HttpResponseRedirect('.')
  values = {
    'outstanding_orders': Order.objects.filter(status=Order.COMPLETED),
    'delivered_orders': Order.objects.filter(status=Order.SHIPPED)[:20]
  }
  return TemplateResponse(request,'store/receipts.html',values)
