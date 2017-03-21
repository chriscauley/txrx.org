import os,django;os.environ['DJANGO_SETTINGS_MODULE']='main.settings';django.setup()

from django.db import models
from djstripe.models import Charge, Transfer
import decimal

Charge.objects.filter(pk=103).update(transfer_id=16)
Charge.objects.filter(pk__in=[343,344,345]).update(transfer_id=51)
def rec(cpk,tid):
  Charge.objects.filter(pk=cpk).update(transfer=Transfer.objects.get(stripe_id=tid))

rec(308,"tr_19ni5JHqBalEWa8135fQwEpp")
rec(304,"tr_19nLcJHqBalEWa81AObPoEuE")

fakes = {
  "tr_19IZTJHqBalEWa81X4pt3dYF": decimal.Decimal("0.38"),
  "tr_19TRQ0HqBalEWa816qnBhJPQ": decimal.Decimal("0.67"),
  "tr_19agPdHqBalEWa81wOAQxCP0": decimal.Decimal("-174.48"),# refund
  "tr_19cUaOHqBalEWa811b6k82ou": decimal.Decimal("-63.11"),
  "tr_19f2DgHqBalEWa812VNm0WPU": decimal.Decimal("-29.13"),
  "tr_19fjYHHqBalEWa814chldz2k": decimal.Decimal("-33.98"),
  "tr_19s5nXHqBalEWa81IC71yINh": decimal.Decimal("-33.98"),
  "tr_19v0sqHqBalEWa81Vx32kQ5h": decimal.Decimal("-87.39"),
  "tr_19vMdRHqBalEWa81qHlAXKyt": decimal.Decimal("-72.82"),
  "tr_19aLk3HqBalEWa81MtGsj0Wx": decimal.Decimal("-47.76"),
  "tr_19xYGxHqBalEWa81NpIkbuVA": decimal.Decimal("-67.67"),
}

for transfer in Transfer.objects.order_by("stripe_timestamp"):
  if transfer.amount < 0:
    continue
  charges = []
  total = fakes.get(transfer.stripe_id,0)
  #print 'tr',transfer.amount
  _q = models.Q(transfer__isnull=True)
  for charge in list(Charge.objects.filter(transfer=transfer))+list(Charge.objects.filter(_q).order_by("stripe_timestamp")):
    if not charge.paid:
      continue
    #print "%s - %s = %s"%(total,transfer.amount,total-transfer.amount)
    total += charge.amount-charge.fee
    charges.append(charge)
    if total == transfer.amount:
      transfer.metadata['charges'] = [c.id for c in charges]
      transfer.metadata['stripe_charges'] = [c.stripe_id for c in charges]
      transfer.metadata['order_ids'] = [c.metadata['order_id'] for c in charges]
      transfer.save()
      for c in charges:
        c.transfer = transfer
        c.save()
      print "yay: %s"%transfer
      break
    if total > transfer.amount:
      print "fail"
      print transfer
      print total
      charges = charges[::-1]
      for i in range(len(charges)):
        s = sum([c.amount-c.fee for c in charges][:i+1])+fakes.get(transfer.stripe_id,0)
        c = charges[i]
        print c.amount-c.fee,'\t',s,'\t',s-transfer.amount,'\t',c.stripe_id,'\t',c.customer.subscriber.email
      exit()
