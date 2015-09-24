from rest_framework import serializers
from membership.models import SubscriptionFlag

class SubscriptionFlagSerializer(serializers.ModelSerializer):
  subscription = serializers.StringRelatedField()
  permissions = classmethod(lambda class_,request: request.user.is_staff)
  class Meta:
    model = SubscriptionFlag
    fields = ['subscription','reason','status','datetime','emailed','days_until_next_action']

subscriptionflag = SubscriptionFlagSerializer

class ActiveFlagSerializer(SubscriptionFlagSerializer):
  @classmethod
  def get_queryset(class_):
    return class_.Meta.model.objects.filter(pk=1) #status__in=SubscriptionFlag.ACTION_CHOICES)
  class Meta:
    model = SubscriptionFlag
    fields = ['subscription','reason','status','datetime','emailed','days_until_next_action']

activeflag = ActiveFlagSerializer
