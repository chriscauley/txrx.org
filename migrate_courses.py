import os,django;os.environ['DJANGO_SETTINGS_MODULE']='main.settings';django.setup()

from course.models import Course, CourseEnrollment
from store.models import Consumable, CourseCheckout
from tool.models import UserCriterion

import datetime

consumable_course_ids = [
  (948, 37),
  (949, 6),
  (857, 48),
  (1029, 62),
  (1105, 180),
  (858, 63),
  (856, 3),
  (952, 95),
  (855, 42),
]

unpaid = 0
nouser = 0

for consumable_id,course_id in consumable_course_ids:
  consumable = Consumable.objects.get(id=consumable_id)
  course = Course.objects.get(id=course_id)
  coursecheckout,new = CourseCheckout.objects.get_or_create(
    name=consumable.name.split(" Check")[0],
    active=True,
    unit_price=consumable.unit_price,
    course=course
  )
  if new:
    print "new CC: %s"%coursecheckout

  orderitems = consumable.orderitem_set.all()
  for oi in orderitems:
    oi.product_name = coursecheckout.get_name()
    oi.product_reference = coursecheckout.get_product_reference()
    oi.product = coursecheckout
    oi.save()
    user = oi.order.user
    if not user:
      nouser += 1
      continue
    if not oi.order.is_paid():
      unpaid += 1
      continue
    coursecheckout.purchase(oi.order.user,oi.quantity)
    ce = CourseEnrollment.objects.get(user=oi.order.user,course=course)
    ce.datetime = oi.order.modified
    ce.save()
    ucs = UserCriterion.objects.filter(user=oi.order.user,criterion=ce.get_criteria())
    if ucs:
      for uc in ucs:
        print ucs.count(),'\t',uc.content_object._meta.model_name,'\t',uc.content_object
        if uc.content_object._meta.model_name == 'user':
          ce.completed = oi.order.modified
          ce.save()
          print "converting %s"%ce
  print orderitems.count(),'\t',consumable

print "unpaid: ",unpaid
print "nouser: ",nouser
