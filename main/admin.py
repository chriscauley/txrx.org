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

from mptt_comments.models import MpttComment
from mptt_comments.admin import MpttCommentsAdmin

admin.site.unregister(FlatPage)
admin.site.unregister(PayPalIPN)
admin.site.unregister(MpttComment)

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

class MpttCommentAdmin(MpttCommentsAdmin):
  list_display = ['_preview']+list(MpttCommentsAdmin.list_display)[1:]
  def _preview(self,obj=None):
    return obj.comment[:25]

admin.site.register(FlatPage,FlatPageAdmin)
admin.site.register(PayPalIPN,CustomIPNAdmin)
admin.site.register(MpttComment,MpttCommentAdmin)

from .signals import *
