import json, os, django
f = open("_shop.json","r");
text = f.read()
text = text.replace('shop.','drop.')
objs=json.loads(text);
f.close();
for o in objs:
  o['fields'].pop('slug',None)
f = open("_drop.json","w")
f.write(json.dumps(objs))
f.close()

"""os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
django.setup()
from drop.models import Product as DropProduct
print DropProduct.objects
from shop.models import Product
Product.objects.all().delete()"""
