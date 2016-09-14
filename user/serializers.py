from django.db.models import Q

from .models import User
from api.serializers import BaseSizzler

class SearchSizzler(BaseSizzler):
  @classmethod
  def get_queryset(class_,request):
    q = request.REQUEST.get('q',None).strip()
    session_id = request.REQUEST.get('session_id',None)
    qs = class_.Meta.model.objects.all()
    if q:
      for word in q.split(" "):
        if not word:
          continue
        _Q = Q()
        for f in ['username','email','paypal_email','first_name','last_name']:
          _Q = _Q | Q(**{f+"__icontains":word})
        qs = qs.filter(_Q).filter(is_active=True).distinct()
        print word,'  ',qs.count()
    return qs.distinct()
  class Meta:
    model = User
    fields = ('username','id','email','paypal_email','get_full_name','rfids')

class StudentSizzler(BaseSizzler):
  class Meta:
    model = User
    fields = ('signature_jsons','enrollment_jsons','locked_criterion_ids','usercriterion_jsons')
