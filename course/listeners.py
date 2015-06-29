from paypal.standard.ipn.signals import payment_was_successful, payment_was_flagged
from django.dispatch import receiver
from django.http import QueryDict
from django.conf import settings
from django.core.mail import send_mail, mail_admins
from django.template.loader import render_to_string

from notify.models import NotifyCourse
from .utils import get_or_create_student

import traceback

_duid='course.signals.handle_successful_payment'
@receiver(payment_was_successful, dispatch_uid=_duid)
def handle_successful_store_payment(sender, **kwargs):
  from shop.models import Product, Order, OrderPayment
  if not params['invoice']:
    return # invoice number means it came from the new django_shop system
  params = QueryDict(sender.query)
  _uid = params.get('custom',None)
  order = Order.objects.get(pk=params['invoice'])
  user,new_user = get_or_create_student(sender.payer_email,u_id=_uid)
  user.active = True
  user.save()
  total = 0
  try:
    item_count = int(params['num_cart_items'])
  except:
    item_count = 1
  products = []
  for i in range(1,item_count+1):
    total += int(float(params['mc_gross_%d'%i]))
    quantity = int(params['quantity%s'%i])
    product = Product.objects.get(int(params['item_number%d'%i]))
    products.append(product)
    product.decrease_stock(quantity)
  order.status = Order.COMPLETED
  order.save()
  payment = OrderPayment.objects.create(
    amount=total,
    payment_method='PayPal',
    transaction_id=sender.txn_id
  )
  [p.save() for p in products] #save decreased stock last, incase of error
  try:
    Cart.objects.get(pk=order.cart_pk).delete()
  except Cart.DoesNotExist:
    pass

@receiver(payment_was_successful, dispatch_uid=_duid)
def handle_successful_payment(sender, **kwargs):
  if params['invoice']:
    return # invoice number means it came from the new django_shop system
  from course.models import Enrollment, Session, reset_classes_json
  #add them to the classes they're enrolled in
  params = QueryDict(sender.query)
  _uid = params.get('custom',None)
  user,new_user = get_or_create_student(sender.payer_email,u_id=_uid)
  user.active = True
  user.save()
  try:
    item_count = int(params['num_cart_items'])
  except:
    item_count = 1

  enrollments = []
  error_sessions = []
  admin_subject = "New course enrollment"
  for i in range(1, item_count+1):
    course_cost = int(float(params['mc_gross_%d'%i]))
    quantity = int(params['quantity%s'%i])

    try:
      session = Session.objects.get(id=int(params['item_number%d' % (i, )]))
    except Session.DoesNotExist:
      mail_admins("Session not found",traceback.format_exc())
      continue
    except ValueError:
      mail_admins("Non-integer session number",traceback.format_exc())
      continue

    enrollment,new = Enrollment.objects.get_or_create(user=user, session=session)
    if enrollment.transaction_ids and (sender.txn_id in enrollment.transaction_ids):
      mail_admins("Multiple transaction ids blocked for enrollment #%s"%enrollment.id,"")
    enrollment.transaction_ids = (enrollment.transaction_ids or "") + sender.txn_id + "|"
    notifys = NotifyCourse.objects.filter(user=user,course=session.course)
    if notifys:
      notifys.delete()
    if new:
      enrollment.quantity = quantity
    else:
      s = "%s seems to have a duplicate enrollment. Please see https://txrxlabs.org/admin/course/session/%s/"
      mail_admins("Course so nice they took it twice",s%(enrollment.user,enrollment.session.pk))
      enrollment.quantity += quantity
    enrollment.save()
    enrollments.append(enrollment)
    if course_cost != session.course.fee * int(quantity):
      l = [
        "PP cost: %s"%course_cost,
        "Session Fee: %s"%session.course.fee,
        "Session Id:%s"%session.id,
        "Quantity:%s"%enrollment.quantity,
        "PP Email:%s"%sender.payer_email,
        "U Email:%s"%user.email,
      ]
      error_sessions.append("\n".join(l))
    if enrollment.session.total_students > enrollment.session.course.max_students:
      s = "Session #%s overfilled. Please see https://txrxlabs.org/admin/course/session/%s/"
      mail_admins("My Course over floweth",s%(enrollment.session.pk,enrollment.session.pk))

  values = {
    'enrollments': enrollments,
    'user': user,
    'new_user': new_user,
  }
  body = render_to_string("email/course_enrollment.html",values)
  send_mail("Course enrollment confirmation",body,settings.DEFAULT_FROM_EMAIL,[user.email])
  send_mail("Course enrollment confirmation",body,settings.DEFAULT_FROM_EMAIL,['chris@lablackey.com'])
  if error_sessions:
    mail_admins("Enrollment Error","\n\n".join(error_sessions))
  reset_classes_json("classes reset during course enrollment")

@receiver(payment_was_flagged, dispatch_uid='course.signals.handle_flagged_payment')
def handle_flagged_payment(sender, **kwargs):
  #email people to let them intervene manually
  handle_successful_payment(sender, **kwargs)
