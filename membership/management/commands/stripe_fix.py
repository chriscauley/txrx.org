import os,django;os.environ['DJANGO_SETTINGS_MODULE']='main.settings';django.setup()

from django.core.management.base import BaseCommand
from django.db import models
from djstripe.models import Charge, Transfer

from drop.payment.backends.stripe_backend import stripe

import decimal

class Command(BaseCommand):
  def handle(self,*args,**kwargs):
    for transfer in Transfer.objects.order_by("stripe_timestamp"):
      po = stripe.BalanceTransaction.all(payout=transfer.stripe_id)
      print transfer.stripe_id
      print po.keys()
      print len(po['data'])
      for d in po['data'][:2]:
        print d
      return
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
          break
        if total > transfer.amount:
          out = ["fail",transfer,total]
          charges = charges[::-1]
          for i in range(len(charges)):
            s = sum([c.amount-c.fee for c in charges][:i+1])+fakes.get(transfer.stripe_id,0)
            c = charges[i]
            out.append(
              c.amount-c.fee,'\t',
              s,'\t',
              s-transfer.amount,'\t',
              c.stripe_id,'\t',
              c.customer.subscriber.email,'\t',
              c.stripe_timestamp
            )
          break
  
