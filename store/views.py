from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import Category

from shop.models import Product
from shop.util.cart import get_or_create_cart

def index(request):
  categories = Category.objects.all()
  values = {
    'categories':categories
  }
  return TemplateResponse(request,'store/index.html',values)

def detail(request,pk,slug):
  product = get_object_or_404(Product,pk=pk)
  values = {
    'product': product,
  }
  return TemplateResponse(request,'store/detail.html',values)

def cart_add(request):
  cart_object = get_or_create_cart(self.request)
  quantity = self.request.GET['item_quantity']
  cart_object.update_quantity(request.POST['pk'], int(quantity))
  return self.put_success()
