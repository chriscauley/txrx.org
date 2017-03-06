from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

from drop.models import OrderItem, Order
from membership.models import Status, Subscription

import datetime, csv

def totals_json(request,format):
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

    # make time period a multiple of resolution because showing half a week sucks
    time_period = time_period-time_period%resolution
    start_date = timezone.now().date() - datetime.timedelta(time_period)

  end_date = start_date+datetime.timedelta(time_period)

  metric = request.GET.get('metric','line_total')
  y2 = []
  if metric in ['line_total','quantity']:
    y = []
    x = []
    for i in range(time_period):
      day = start_date + datetime.timedelta(i)
      _items = order_items.filter(order__created__gte=day,order__created__lt=day+datetime.timedelta(1))
      y.append(sum(_items.values_list(metric,flat=True)))
      x.append(day.strftime("%Y-%m-%d"))
  elif metric in ['new_students','new_members']:
    x = [start_date + datetime.timedelta(i) for i in range(time_period)]
    if metric == 'new_students':
      users = get_user_model().objects.filter(enrollment__isnull=False).distinct()
      firsts = [u.enrollment_set.all().order_by("-datetime")[0].datetime.date() for u in users]
      cancels = []
    elif metric == "new_members":
      users = get_user_model().objects.filter(subscription__isnull=False).distinct()
      firsts = [u.subscription_set.all().order_by("created")[0].created.date() for u in users]
      _s = [u.subscription_set.all().order_by("-created")[0] for u in users]
      cancels = [s.paid_until for s in _s if s.canceled]
      y2 = {d:0 for d in x}
      for d in cancels:
        if d.date() in y2:
          y2[d.date()] += 1
      x, y2 = zip(*sorted(y2.items()))
    y = {d:0 for d in x}
    for d in firsts:
      if d in y:
        y[d] += 1
    x, y = zip(*sorted(y.items()))
    x = [d.strftime("%Y-%m-%d") for d in x]
  elif metric == "classes_per_student":
    students = {}
    items = order_items.filter(order__created__gte=start_date,order__created__lte=end_date)
    for user_id,quantity in items.values_list("order__user_id","quantity"):
      if not user_id:
        continue
      students[user_id] = students.get(user_id,0) + quantity
    x,y = zip(*sorted(students.items()))
  elif metric in ['member_payments','all_payments']:
    x = []
    y2 = []
    y = []
    statuses = Status.objects.all()
    for i in range(time_period):
      day = start_date + datetime.timedelta(i)
      next_day = day + datetime.timedelta(1)
      _statuses = statuses.filter(datetime__gte=day,datetime__lte=next_day)
      x.append(day.strftime("%Y-%m-%d"))
      y.append(sum(_statuses.filter(subscription__months=1).values_list('amount',flat=True)))
      y2.append(sum(_statuses.exclude(subscription__months=1).values_list('amount',flat=True)))
      if metric == 'all_payments':
        y[-1] += y2[-1] # yearly
        _items = order_items.filter(order__created__gte=day,order__created__lt=day+datetime.timedelta(1))
        y[-1] += sum(_items.values_list('line_total',flat=True))
  _x = []
  _y2 = []
  _y = []
  if 'metric' != 'classes_per_student':
    if resolution == 'month':
      month = None
      for i,day in enumerate(x):
        if month != day.split("-")[1]:
          year,month,day = day.split("-")
          _x.append("-".join([year,month]))
          _y.append(0)
          if y2:
            _y2.append(0)
        _y[-1] += y[i]
        if _y2:
          _y2[-1] += y2[i]
    elif resolution != 1:
      for i,day in enumerate(x):
        if not i%resolution:
          _x.append(day)
          _y.append(0)
          if y2:
            _y2.append(0)
        _y[-1] += y[i]
        if _y2:
          _y2[-1] += y2[i]
  if format == 'table':
    table = "\n".join(["%s\t%s\t%s\t"%t for t in zip(x,y,y2)])
    table2 = "\n".join(["%s\t%s\t%s\t"%t for t in zip(_x,_y,_y2)])
    return HttpResponse("<pre>%s</pre>2<pre>%s</pre>"%(table,table2))

  x = _x or x
  y = _y or y
  y2 = _y2 or y2

  if format == 'csv':
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_%s-%s.csv"'%(metric,start_date,end_date)
    writer = csv.writer(response)
    if y2:
      rows = zip(x,y,y2)
    else:
      rows = zip(x,y)
    for row in zip(x,y):
      writer.writerow(row)
    return response
  return JsonResponse({
    'x': x,
    'y': y,
    'y2': y2,
    'zipt': zip(x,y,y2)
  })
