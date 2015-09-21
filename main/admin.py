from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import *
from django.core.urlresolvers import reverse
from django import forms

from media.admin import TaggedPhotoInline
from membership.models import UserMembership

from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.ipn.admin import PayPalIPNAdmin

admin.site.unregister(FlatPage)
admin.site.unregister(PayPalIPN)

TEMPLATE_CHOICES = (
  ('','HTML'),
  ('flatpages/markdown.html','MarkDown'),
)

class FlatPageForm(forms.ModelForm):
  template_name = forms.CharField(label="Render As",help_text="",required=False)
  def __init__(self, *args, **kwargs):
    super(FlatPageForm, self).__init__(*args, **kwargs)
    self.fields['template_name'].widget = forms.Select(choices=TEMPLATE_CHOICES)
  class Meta:
    model = FlatPage
    exclude = ()

class FlatPageAdmin(FlatPageAdmin):
  list_display = ('url','title','template_name')
  form = FlatPageForm
  inlines = [TaggedPhotoInline]

class UserMembershipInline(admin.StackedInline):
  extra = 0
  has_add_permission = lambda self,request: False
  has_delete_permission = lambda self,*args: False
  model = UserMembership

class CustomIPNAdmin(PayPalIPNAdmin):
  fieldsets = PayPalIPNAdmin.fieldsets
  fieldsets[0][1]['fields'].append('view_redirect')
  fieldsets[0][1]['fields'].append('view_IPN')
  readonly_fields = PayPalIPNAdmin.readonly_fields + ('view_redirect','view_IPN')
  list_display = PayPalIPNAdmin.list_display + ['txn_type','subscr_id']
  list_filter = list(PayPalIPNAdmin.list_filter) + ['txn_type']
  def subscr_id(self,obj):
    data = QueryDict(obj.query)
    return data.get('subscr_id',None) or data.get('recurring_payment_id',None)
  def view_redirect(self,obj):
    link = '<a href="%s">View Redirect</a>'
    return link%(reverse('paypal_redirect')+"?"+obj.query)
  view_redirect.allow_tags = True
  def view_IPN(self,obj):
    lines = [
      "django.jQuery.post(",
      "'/tx/rx/ipn/handler/',"
      "django.jQuery('#id_query').val(),"
      "function(){django.jQuery('#emulate_ipn').replaceWith('Done')}"
      ")"
    ]
    onclick = ''.join(lines)
    link = '<a href="javascript:;" id="emulate_ipn" onclick="%s">Emulate Post</a>'%onclick
    return link
  view_IPN.allow_tags = True

admin.site.register(FlatPage,FlatPageAdmin)
admin.site.register(PayPalIPN,CustomIPNAdmin)

from .signals import *
