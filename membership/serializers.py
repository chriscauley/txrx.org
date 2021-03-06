from rest_framework import serializers

from lablackey.api.serializers import BaseSizzler
from membership.models import Flag

class FlagSizzler(BaseSizzler):
  subscription = serializers.StringRelatedField()
  permissions = classmethod(lambda class_,request: request.user.is_staff)
  class Meta:
    model = Flag
    fields = ['subscription','reason','status','datetime','emailed','days_until_next_action']

class ActiveFlagSizzler(FlagSizzler):
  @classmethod
  def get_queryset(class_,request=None):
    return class_.Meta.model.objects.filter(status__in=Flag.PAYMENT_ACTIONS)
  class Meta:
    model = Flag
    fields = ['subscription','reason','status','datetime','emailed','days_until_next_action','last_datetime','user_id']
