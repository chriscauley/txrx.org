from django import template
from store.models import Consumable, CourseCheckout

register = template.Library()

@register.filter
def filter_order_by_model(orders,model_name):
  for o in orders:
    for i in o.items.all():
      print i.product._meta.model_name, i.product.polymorphic_ctype.model
  out = [(o,o.items.filter(product__polymorphic_ctype__model=model_name)) for o in orders]
  print filter(lambda o: o[1],out)
  return filter(lambda o: o[1],out)

