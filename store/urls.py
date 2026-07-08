from django.urls import include, path, re_path

from . import views
import drop.urls

urlpatterns = [
  path('',views.index,name='product_list'),
  path('categories.js',views.categories_json,name='categories_json'),
  re_path(r'^coursecheckout/(\d+).json$',views.coursecheckout_ajax),
  path('start_checkout/',views.start_checkout,name='start_checkout'),

  path('receipts/',views.receipts,name='receipts'),
  path('admin/',views.admin_page,name='admin_page'),
  path('admin/add/',views.admin_add,name='admin_add'),
  re_path(r'^admin/products.json',views.admin_products_json,name='admin_products_json'),
  path('', include(drop.urls)),
]
