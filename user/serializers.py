from django.db.models import Q

from .models import User
from tool.models import UserCriterion
from api.serializers import BaseSizzler

class SearchSizzler(BaseSizzler):
  @classmethod
  def get_queryset(class_,request):
    q = request.REQUEST.get('q',None).strip()
    session_id = request.REQUEST.get('session_id',None)
    qs = class_.Meta.model.objects.all()
    if q:
      _Q = Q()
      for f in ['username','email','usermembership__paypal_email','first_name','last_name']:
        _Q = _Q | Q(**{f+"__icontains":q})
      qs = qs.filter(_Q).filter(is_active=True).distinct()
    return qs
  class Meta:
    model = User
    fields = ('username','id','email','paypal_email','get_full_name','rfids')

class StudentSizzler(BaseSizzler):
  class Meta:
    model = User
    fields = ('signature_jsons','enrollment_jsons','locked_criterion_ids','criterion_ids')
