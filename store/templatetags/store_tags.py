from django import template
from store.models import Consumable, CourseCheckout
from drop.models import Order

register = template.Library()

@register.filter
def filter_order_by_model(orders,model_name):
  out = [(o,o.items.filter(product__polymorphic_ctype__model=model_name)) for o in orders]
  return filter(lambda o: o[1],out)

@register.filter
def get_order_pk(enrollment):
  coursecheckout = CourseCheckout.objects.get(course=enrollment.course)
  for order in  Order.objects.filter(user=enrollment.user,items__product=coursecheckout):
    if order.is_paid():
      return order.pk
  print coursecheckout
