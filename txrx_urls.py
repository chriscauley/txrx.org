from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test
import lablackey.views

from django.template.response import TemplateResponse
from djstripe.models import Transfer
from drop.models import Order
from drop.giftcard.models import GiftCardProduct
from store.models import Consumable, CourseCheckout
from course.models import SessionProduct

@user_passes_test(lambda u: u.is_superuser)
def transfers(request):
  transfers = []
  classes = (SessionProduct,Consumable,CourseCheckout,GiftCardProduct)
  for transfer in Transfer.objects.all():
    totals = {c:0 for c in classes}
    for charge in transfer.charge_set.all():
      charge_total = charge.amount - charge.fee
      order = Order.objects.get(pk=charge.metadata['order_id'])
      for item in order.items.all():
        item_ratio = item.line_total / order.order_total
        if isinstance(item.product,classes):
          totals[item.product.__class__] += item_ratio*charge_total
        else:
          print item.product.__class__,transfer.stripe_id
    _totals = [totals[c] for c in classes]
    transfers.append((transfer,_totals,transfer.amount-sum(_totals)))
  sums = [0,0,0,0]
  for transfer,totals,error in transfers:
    for i,t in enumerate(totals):
      sums[i] += t
  values = {
    'transfers': transfers,
    'labels': ["transfer","transfer.total (error)","classes","consumables","checkouts","giftcards"],
    'sums': sums,
  }
  return TemplateResponse(request,"txrx/transfers.html",values)

urlpatterns = [
  url(r'^work/$',lablackey.views.single_page_app),
  url(r'^txrx/transfers/$',transfers)
]
