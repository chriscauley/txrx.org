import os, django, datetime, arrow
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

django.setup()
from membership.models import Subscription, Level, Status
from django.db.models import Q

levels = list(Level.objects.all())[1:-3]
rows = [["Year","Month"] + [str(p) for p in levels] + [""] + [str(p) for p in levels] + ["total"]]

for year in range(2012,2017):
  for month in range(1,13):
    row = [str(year),str(month)]
    cash = [""]
    start = arrow.get(year,month,1).datetime
    end = arrow.get(year,month,1).replace(months=1).datetime
    if start > arrow.get():
      break
    for level in levels:
      subscriptions = Subscription.objects.filter(created__lte=start)
      subscriptions = subscriptions.filter(Q(canceled__gte=start) | Q(canceled=None),level=level).count()
      row.append(str(subscriptions))
      statuses = Status.objects.filter(datetime__gte=start,datetime__lte=end)
      statuses = statuses.filter(subscription__level=level).distinct()
      cash.append(str(sum([s.amount for s in statuses])))
    statuses = Status.objects.filter(datetime__gte=start,datetime__lte=end)
    cash.append(str(sum([s.amount for s in statuses])))
    row += cash
    rows.append(row)

print "\n".join([','.join(r) for r in rows])
