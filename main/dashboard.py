from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone

from drop.models import OrderItem, Order

import datetime

def totals_json(request):
  order_items = OrderItem.objects.filter(order__status__gte=Order.PAID)
  if request.GET.get('product_types',"").isdigit():
    order_items = order_items.filter(product__polymorphic_ctype_id=request.GET['product_types'])

  #! TODO this could be dynamic
  if request.GET.get("time_period","").isdigit():
    time_period = int(request.GET.get('time_period',None) or 180)
  else:
    time_period = (timezone.now()-Order.objects.all().order_by("created")[0].created).days
  start_date = timezone.now().date() - datetime.timedelta(time_period)

  metric = request.GET.get('metric','line_total')
  if metric in ['line_total','quantity']:
    data = []
    days = []
    for i in range(time_period):
      day = start_date + datetime.timedelta(i)
      _items = order_items.filter(order__created__gte=day,order__created__lt=day+datetime.timedelta(1))
      data.append(sum(_items.values_list(metric,flat=True)))
      days.append(day.strftime("%Y-%m-%d"))
  elif metric == 'new_students':
    days = [start_date + datetime.timedelta(i) for i in range(time_period)]
    users = get_user_model().objects.filter(enrollment__isnull=False).distinct()
    first_enrollments = [u.enrollment_set.all().order_by("-datetime")[0].datetime.date() for u in users]
    data = {d:0 for d in days}
    for d in first_enrollments:
      if d in data:
        data[d] += 1
    zip(*sorted(data.items()))
    days, data = zip(*sorted(data.items()))
  return JsonResponse({
    'data': data,
    'days': days,
  })
