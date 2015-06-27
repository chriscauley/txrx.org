import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

from store.models import Consumable, Category
import django
django.setup()

f = open('TX-RX_STOCK_PRICE_LIST_-_Sheet1.csv','r')
lines = [l.split(',') for l in f.readlines()]
f.close()

for line in lines:
  if line[0]:
    category, new = Category.objects.get_or_create(name=line[0])
    continue
  defaults = {
    'part_number': line[3],
    'part_style': line[4],
    'unit_price': line[5] or 0,
  }
  name= line[1]
  slug = name.lower().replace(' ','_')
  product,new = Consumable.objects.get_or_create(name=name,slug=slug,defaults=defaults)
  product.categories.add(category)
  product.save()
