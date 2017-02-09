from django.http import JsonResponse
from django.utils import timezone

from drop.models import OrderItem, Order

import datetime

def totals_json(request):
  order_items = OrderItem.objects.filter(order__status__gte=Order.PAID)
  print order_items.count()
  if 'ctype' in request.GET:
    order_items = order_items.filter(product__polymorphic_ctype_id=request.GET)

  #! TODO this could be dynamic
  days = 180
  start_date = timezone.now().date() - datetime.timedelta(days)

  money = []
  quantity = []
  days = []
  for i in range(180):
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
