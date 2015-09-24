from rest_framework import serializers
from membership.models import SubscriptionFlag

class SubscriptionFlagSerializer(serializers.HyperlinkedModelSerializer):
  subscription = serializers.StringRelatedField()
  class Meta:
    model = SubscriptionFlag
