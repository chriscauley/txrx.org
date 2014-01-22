from paypal.standard.ipn.signals import payment_was_successful, payment_was_flagged
from django.dispatch import receiver
from django.http import QueryDict
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, mail_admins
from .utils import get_or_create_student
import traceback

@receiver(payment_was_successful, dispatch_uid='course.signals.handle_successful_payment')
def handle_successful_payment(sender, **kwargs):
  from course.models import Enrollment, Session
  #add them to the classes they're enrolled in
  params = QueryDict(sender.query)
  user = get_or_create_student(sender.payer_email,u_id=params.get('custom',None))
  try:
    class_count = int(params['num_cart_items'])
  except:
    class_count = 1

  for i in range(1, class_count+1):
    section_cost = int(float(params['mc_gross_%d'%i]))
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
    if new:
      enrollment.quantity = quantity
    else:
      enrollment.quantity += quantity
    enrollment.save()
    if True: #section_cost != session.section.fee:
      # email chris for verification
      l = ["PP cost: %s"%section_cost,
           "Session Fee: %s"%session.section.fee,
           "Session Id:%s"%session.id,
           "Quantity:%s"%enrollment.quantity,
           "PP Email:%s"%sender.payer_email,
           "U Email:%s"%user.email)
      ]
      m = '\n'.join(l)
      mail_admins("New course enrollment",m)

@receiver(payment_was_flagged, dispatch_uid='course.signals.handle_flagged_payment')
def handle_flagged_payment(sender, **kwargs):
  #email people to let them intervene manually
  handle_successful_payment(sender, **kwargs)
