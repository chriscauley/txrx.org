import os,django;os.environ['DJANGO_SETTINGS_MODULE']='main.settings';django.setup()

from django.db import models
from djstripe.models import Charge, Transfer
import decimal

Charge.objects.filter(pk=103).update(transfer_id=16)
Charge.objects.filter(pk__in=[343,344,345]).update(transfer_id=51)
def rec(cpk,tid):
  Charge.objects.filter(pk=cpk).update(transfer=Transfer.objects.get(stripe_id=tid))
def rec2(cids,tid):
  for cid in cids:
    cid = cid.split("/")[-1]
    Charge.objects.filter(stripe_id=cid).update(transfer=Transfer.objects.get(stripe_id=tid))

rec(308,"tr_19ni5JHqBalEWa8135fQwEpp")
rec(304,"tr_19nLcJHqBalEWa81AObPoEuE")

rec2([
  'https://dashboard.stripe.com/payments/ch_19zq7PHqBalEWa81gBBN7dDP',
  'https://dashboard.stripe.com/payments/ch_19zq4zHqBalEWa81cLzEK9Ud',
  'https://dashboard.stripe.com/payments/ch_19znF8HqBalEWa81zV0ldnZi',
  'https://dashboard.stripe.com/payments/ch_19zd4hHqBalEWa81RgcGrvM5',
  'https://dashboard.stripe.com/payments/ch_19zcQdHqBalEWa81AbOXoToZ',
  'https://dashboard.stripe.com/payments/ch_19zcLrHqBalEWa81xEp4b2DC',
  ],'po_1A05beHqBalEWa81Njy9qAJO')
rec2([
  'https://dashboard.stripe.com/payments/ch_19za6qHqBalEWa81nrnavRor',
  'https://dashboard.stripe.com/payments/ch_19zTeDHqBalEWa81FGpv1wDp',
  'https://dashboard.stripe.com/payments/ch_19zTFIHqBalEWa81G6LlsOo7',
  'https://dashboard.stripe.com/payments/ch_19zSaHHqBalEWa81CYbYS2rl',
  'https://dashboard.stripe.com/payments/ch_19zQAPHqBalEWa81C8D1rEpv',
  'https://dashboard.stripe.com/payments/ch_19zGD6HqBalEWa81wgHhhKvA',
  'https://dashboard.stripe.com/payments/ch_19zD0jHqBalEWa81Qw0Vw3fR',
  'https://dashboard.stripe.com/payments/ch_19z7yCHqBalEWa81QzxoYUk7',
  'https://dashboard.stripe.com/payments/ch_19yXvpHqBalEWa81r4HA3eKc',
],'po_19zjEkHqBalEWa81fJ7jdMAZ')
rec2(["ch_1AsEGkHqBalEWa81hQKF3e2g"],"po_1AtAhUHqBalEWa810xxx4z6F")
rec2(["ch_1ArxtsHqBalEWa81KTfKoGiA"],"po_1Aso0WHqBalEWa81yPCVYFT0")
rec2([
  'https://dashboard.stripe.com/payments/ch_1Ayn0cHqBalEWa818uMwqJej',
  'https://dashboard.stripe.com/payments/ch_1AyqAIHqBalEWa81PARwPyjz',
  'https://dashboard.stripe.com/payments/ch_1Aylf8HqBalEWa819ADoMamT',
  'https://dashboard.stripe.com/payments/ch_1AyUsbHqBalEWa81WnN9tkkl',
  'https://dashboard.stripe.com/payments/ch_1AyNyvHqBalEWa81d8gLUqkG',
  'https://dashboard.stripe.com/payments/ch_1AxnS5HqBalEWa8119SLiwvt',
  'https://dashboard.stripe.com/payments/ch_1Axk1QHqBalEWa81tQXqPBCy',
],"po_1Ayz3sHqBalEWa817kHCr8sB")
"""
  '',
  ],'po_19zjEkHqBalEWa81fJ7jdMAZ')
rec2(["ch_1AsEGkHqBalEWa81hQKF3e2g"],"po_1AtAhUHqBalEWa810xxx4z6F")
<<<<<<< Updated upstream
"""

fakes = {
  "po_19zjEkHqBalEWa81fJ7jdMAZ": decimal.Decimal(8739+12623)*-1,
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
  "po_19zjEkHqBalEWa81fJ7jdMAZ": decimal.Decimal("-213.62"),
  'po_1A0RiwHqBalEWa81oxOOXbQu': decimal.Decimal("-38.84"),
  "po_1A5AYGHqBalEWa81tInML6UH": decimal.Decimal("-29.13"),
  "po_1A5WeRHqBalEWa81kAlQlp8X": decimal.Decimal("-67.97"),
  "po_1AD5DoHqBalEWa81l9dZzydt": decimal.Decimal("-53.4"),
  "po_1AH3m3HqBalEWa817BmJhmSR": decimal.Decimal("-48.25"),
  "po_1AJxvkHqBalEWa81wOkSclNp": decimal.Decimal("-116.52"),
  "po_1AZC3mHqBalEWa81TbEbEiKZ": decimal.Decimal("-33.98"),
  "po_1AOfoeHqBalEWa81wc5A4S7f": decimal.Decimal("-38.54"),
  "po_1AU8INHqBalEWa81mcSELMn6": decimal.Decimal("-53.40"),
  "po_1AVwVbHqBalEWa81tpNh5sFo": decimal.Decimal("-21.84"),
  "po_1AlWcXHqBalEWa81vyscB449": decimal.Decimal("-193.00"),
  "po_1Ao4OFHqBalEWa810mvQKQ9z": decimal.Decimal("-12.62"),
  "po_1AqycIHqBalEWa81H9XIjCyJ": decimal.Decimal("-174.78"),
  "po_1Ayz3sHqBalEWa817kHCr8sB": decimal.Decimal("-770.43"),
  "po_1B0nEUHqBalEWa81AD87jsUs": decimal.Decimal("-96.80"),
  "po_1B1sboHqBalEWa81tro9gK7V": decimal.Decimal("-77.08"),
  "po_1B43ZIHqBalEWa812icLW2iD": decimal.Decimal("-140.19"),
  "po_1B8mX7HqBalEWa81kdqpVgkk": decimal.Decimal("-218.17"),
  "po_1B98MdHqBalEWa81nPgosXmg": decimal.Decimal("-53.10"),
  "": decimal.Decimal("0"),
}

for transfer in Transfer.objects.order_by("stripe_timestamp"):
  if transfer.amount < 0:
    continue
  charges = []
  total = fakes.get(transfer.stripe_id,0)
  #print 'tr',transfer.amoun
  if 'order_ids' in transfer.metadata:
    continue
  _q = models.Q(transfer__isnull=True)
  for charge in list(Charge.objects.filter(transfer=transfer))+list(Charge.objects.filter(_q).order_by("stripe_timestamp")):
    if not charge.paid:
      continue
    #print "%s - %s = %s"%(total,transfer.amount,total-transfer.amount)
    total += charge.amount-charge.fee
    charges.append(charge)
    print total,'\t',transfer.amount
    if total == transfer.amount:
      transfer.metadata['charges'] = [c.id for c in charges]
      transfer.metadata['stripe_charges'] = [c.stripe_id for c in charges]
      transfer.metadata['order_ids'] = [c.metadata['order_id'] for c in charges if 'order_id' in c.metadata]
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
        print c.amount-c.fee,'\t',s,'\t',s-transfer.amount,'\t',c.stripe_id,'\t',c.customer.subscriber.email,'\t',c.stripe_timestamp
      exit()
