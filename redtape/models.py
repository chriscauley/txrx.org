from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db import models

from tool.models import CriterionModel

class Document(models.Model):
  name = models.CharField(max_length=512)
  content = models.TextField(null=True,blank=True)
  _ht = "If checked, user must log into site before viewing/signing document"
  login_required = models.BooleanField(default=False,help_text=_ht)
  __unicode__ = lambda self: self.name
  get_absolute_url = lambda self: reverse('signed_document',args=[self.id,slugify(self.name)])

class Signature(CriterionModel):
  document = models.ForeignKey(Document)
  automatic = True
  date_typed = models.CharField("Type Todays Date",max_length=64)
  name_typed = models.CharField("Type Your Name",max_length=128)
  signature = models.ImageField(upload_to="signatures/%m-%d-%y")
  user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True)
  get_criteria = lambda self: self.document.criterion_set.all()
  __unicode__ = lambda self: "%s: %s - %s"%(self.document,self.name_typed,self.date_typed)
  @property
  def as_json(self):
    return {
      'id': self.id,
      'document_name': unicode(self.document),
      'completed': unicode(self.completed or ''),
    }
