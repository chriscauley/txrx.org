from django.db.models import Q

from .models import User
from api.serializers import BaseSizzler

class SearchSizzler(BaseSizzler):
  @classmethod
  def get_queryset(class_,request):
    qs = class_.Meta.model.objects.keyword_search(request.REQUEST.get('q',""))
    if 'user_id' in request.GET:
      qs = qs.filter(id=request.GET['user_id'])
    return qs.distinct()
  class Meta:
    model = User
    fields = ('username','id','email','paypal_email','get_full_name','rfids')

class StudentSizzler(BaseSizzler):
  class Meta:
    model = User
    fields = ('signature_jsons','enrollment_jsons','locked_criterion_ids','usercriterion_jsons')
