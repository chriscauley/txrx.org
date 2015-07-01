from django.conf.urls import url, patterns, include

urlpatterns = patterns(
  'store.views',
  url(r'^$','index',name='product_list'),
  url(r'^start_checkout/$','start_checkout',name='start_checkout'),
  url(r'^edit/$','cart_edit',name='cart_edit'),
  url(r'^(\d+)/([^/]+)/$','detail',name='product_detail'),

  url(r'^admin/$','admin_page',name='admin_page'),
  url(r'^receipts/$','receipts',name='receipts'),
  url(r'^admin/products.json','admin_products_json',name='admin_products_json'),
  #url(r'', include('shop.urls')),
)
