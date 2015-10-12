from django.db.models import Q
from rest_framework import serializers

from .models import User
from api.serializers import BaseSizzler

class SearchSizzler(BaseSizzler):
  permissions = classmethod(lambda class_,request: request.user.is_staff)
  @classmethod
  def get_queryset(class_,request):
    q = request.REQUEST.get('q',None)
    qs = class_.Meta.model.objects.all()
    if q:
      _Q = Q(username=q) | Q(usermembership__paypal_address=q) | Q(rfid=q) | Q(first_name=q) | Q(last_name=q)
      qs = qs.objects.filter(_Q).filter(is_active=True)
    return qs
  class Meta:
    model = User
    fields = ('username','pk','email')
