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

  if request.GET.get('resolution',None) == "month":
    start_date = start_date.replace(day=1)
    resolution = 'month'
  else:
    resolution = int(request.GET.get('resolution',None) or 1)

  metric = request.GET.get('metric','line_total')
  if metric in ['line_total','quantity']:
    y = []
    x = []
    for i in range(time_period):
      day = start_date + datetime.timedelta(i)
      _items = order_items.filter(order__created__gte=day,order__created__lt=day+datetime.timedelta(1))
      y.append(sum(_items.values_list(metric,flat=True)))
      x.append(day.strftime("%Y-%m-%d"))
  elif metric == 'new_students':
    x = [start_date + datetime.timedelta(i) for i in range(time_period)]
    users = get_user_model().objects.filter(enrollment__isnull=False).distinct()
    first_enrollments = [u.enrollment_set.all().order_by("-datetime")[0].datetime.date() for u in users]
    y = {d:0 for d in x}
    for d in first_enrollments:
      if d in y:
        y[d] += 1
    zip(*sorted(y.items()))
    x, y = zip(*sorted(y.items()))
  elif metric == "classes_per_student":
    students = {}
    end_date = start_date+datetime.timedelta(time_period)
    items = order_items.filter(order__created__gte=start_date,order__created__lte=end_date)
    for user_id,quantity in items.values_list("order__user_id","quantity"):
      if not user_id:
        continue
      students[user_id] = students.get(user_id,0) + quantity
    x,y = zip(*sorted(students.items()))
    return JsonResponse({
      'y': y,
      'x': x,
    })

  _x = []
  _y = []
  if resolution == 'month':
    month = None
    for i,day in enumerate(x):
      if month != day.split("-")[1]:
        year,month,day = day.split("-")
        _x.append("-".join([year,month]))
        _y.append(0)
      _y[-1] += y[i]
  elif resolution != 1:
    for i,day in enumerate(x):
      if not i%resolution:
        _x.append(day)
        _y.append(0)
      _y[-1] += y[i]

  x = _x or x
  y = _y or y
  return JsonResponse({
    'y': y,
    'x': x,
  })
