from django.conf.urls import url, patterns, include

import views
import drop.urls

urlpatterns = [
  url(r'^$',views.index,name='product_list'),
  url(r'^categories.js$',views.categories_json,name='categories_json'),
  url(r'^start_checkout/$',views.start_checkout,name='start_checkout'),

  url(r'^receipts/$',views.receipts,name='receipts'),
  url(r'^checkouts/$',views.checkouts,name='checkouts'),
  url(r'^admin/$',views.admin_page,name='admin_page'),
  url(r'^admin/add/$',views.admin_add,name='admin_add'),
  url(r'^admin/products.json',views.admin_products_json,name='admin_products_json'),
  url(r'', include(drop.urls)),
]
