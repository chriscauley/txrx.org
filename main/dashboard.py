from django.http import JsonResponse
from django.utils import timezone

from drop.models import OrderItem, Order

import datetime

def totals_json(request):
  order_items = OrderItem.objects.filter(order__status__gte=Order.PAID)
  print order_items.count()
  if request.GET.get('product_types',"").isdigit():
    order_items = order_items.filter(product__polymorphic_ctype_id=request.GET['product_types'])

  #! TODO this could be dynamic
  if request.GET.get("time_period","").isdigit():
    time_period = int(request.GET.get('time_period',None) or 180)
  else:
    time_period = (timezone.now()-Order.objects.all().order_by("created")[0].created).days
  start_date = timezone.now().date() - datetime.timedelta(time_period)

  money = []
  quantity = []
  days = []
  for i in range(time_period):
    day = start_date + datetime.timedelta(i)
    _items = order_items.filter(order__created__gte=day,order__created__lt=day+datetime.timedelta(1))
    money.append(sum(_items.values_list('line_total',flat=True)))
    quantity.append(sum(_items.values_list('quantity',flat=True)))
    days.append(day.strftime("%Y-%m-%d"))
  return JsonResponse({
    'money': money,
    'quantity': quantity,
    'days': days,
  })
