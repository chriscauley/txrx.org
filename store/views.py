from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Category, reset_products_json

from shop.models import Product, CartItem
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
  
  return HttpResponse('')

