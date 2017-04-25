from api.serializers import BaseSizzler
from django.utils import timezone

from .models import Notification, Follow

import json

class FeedSizzler(BaseSizzler):
  @classmethod
  def get_queryset(class_,request):
    qs = class_.Meta.model.objects
    if not request.user.is_authenticated():
      return qs.none()
    return qs.filter(user=request.user)
  #def __delete__(self):
  #  self.Meta.model.objects.filter(url=None).update(read=timezone.now())
  class Meta:
    model = Notification
    fields = Notification.json_fields

class FollowSizzler(BaseSizzler):
  @classmethod
  def get_queryset(class_,request):
    qs = class_.Meta.model.objects
    if not request.user.is_authenticated():
      return qs.none()
    return qs.filter(user=request.user)
  class Meta:
    model = Follow
    fields = Follow.json_fields
