import django,os; os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings';django.setup()
from django.http import QueryDict

from course.models import Enrollment
from drop.models import Order, OrderPayment
from lablackey.utils import latin1_to_ascii 
from paypal.standard.ipn.models import PayPalIPN

from decimal import Decimal
Order.objects.filter(pk__gt=3000).delete()
for enrollment in Enrollment.objects.exclude(transaction_ids__isnull=True):
  for txn_id in enrollment.transaction_ids.split("|"):
    if not txn_id:
      continue
    ipn = PayPalIPN.objects.filter(txn_id=txn_id)[0]
    order_payments = OrderPayment.objects.filter(transaction_id=txn_id)
    params = QueryDict(latin1_to_ascii(ipn.query))
    if order_payments:
      order = order_payments[0].order
    else:
      order = Order.objects.create(
        order_total=params['mc_gross'],
        order_subtotal=params['mc_gross'],
        user=enrollment.user,
      )
      order.created=enrollment.datetime
      order.updated=enrollment.datetime
      order.status = order.PAID
      order.save()
      order_payments = [OrderPayment.objects.create(
        order=order,
        transaction_id=txn_id,
        backend='paypal',
        description='backfilled paypal payment',
      )]
      for s in [s for s in params.keys() if s.startswith("item_name")]:
        session = enrollment.session
        sessionproduct = session.sessionproduct
        number = s[-1]
        total = params['mc_gross_'+s[-1]]
        order_item = order.items.create(
          product_reference=sessionproduct.pk,
          product_name=params[s],
          product=sessionproduct,
          unit_price=Decimal(total)/enrollment.quantity,
          quantity=enrollment.quantity,
          line_subtotal=total,
          line_total=total
        )
        print "Order created: ",order,'  ',order.created
