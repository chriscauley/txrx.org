from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import *
from django.core.urlresolvers import reverse
from django import forms
from django.http import QueryDict

from main.models import FlatPagePrice, Rate
from media.admin import TaggedPhotoInline
from membership.models import UserMembership

from lablackey.utils import latin1_to_ascii
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

try:
  @admin.register(Rate)
  class RateAdmin(admin.ModelAdmin):
    pass
except:
  pass

class FlatPagePriceInline(admin.TabularInline):
  model = FlatPagePrice
  extra = 0

class FlatPageAdmin(FlatPageAdmin):
  list_display = ('url','title','template_name')
  form = FlatPageForm
  inlines = [TaggedPhotoInline]
  def get_inline_instances(self,request,obj=None):
    # Just like the default behavior, but uses FlatPagePriceInline for object 13
    inlines = self.inlines
    if obj and obj.pk == 13:
      inlines = [FlatPagePriceInline]
    inline_instances = []
    for inline_class in inlines:
      inline = inline_class(self.model, self.admin_site)
      if request:
        if not (inline.has_add_permission(request) or
                inline.has_change_permission(request, obj) or
                inline.has_delete_permission(request, obj)):
          continue
        if not inline.has_add_permission(request):
          inline.max_num = 0
      inline_instances.append(inline)
    return inline_instances

class UserMembershipInline(admin.StackedInline):
  extra = 0
  has_add_permission = lambda self,request: False
  has_delete_permission = lambda self,*args: False
  model = UserMembership

class CustomIPNAdmin(PayPalIPNAdmin):
  fieldsets = PayPalIPNAdmin.fieldsets[:]
  if not 'query_list' in fieldsets[0][1]['fields']:
    fieldsets[0][1]['fields'].append(('view_redirect','view_IPN'))
    fieldsets[0][1]['fields'].append('query_list')
  readonly_fields = PayPalIPNAdmin.readonly_fields + ('view_redirect','view_IPN','query_list')
  list_display = ['__unicode__','_info','created_at']
  def _info(self,obj):
    attrs = [
      ('','txn_type'),
      ('Flag','flag_info'),
      ('Invoice #','invoice'),
      ('Custom','custom'),
      ('Subscr_id','subscr_id')
    ]
    return "<br/>".join(["%s %s"%(a,getattr(obj,b)) for a,b in attrs if getattr(obj,b)])
  _info.allow_tags = True
  def subscr_id(self,obj):
    data = QueryDict(obj.query)
    return data.get('subscr_id',None) or data.get('recurring_payment_id',None)
  def view_redirect(self,obj):
    link = '<a href="%s">View Redirect</a>'
    return link%(reverse('paypal_redirect')+"?"+obj.query)
  view_redirect.allow_tags = True
  def query_list(self,obj):
    try:
      params = QueryDict(latin1_to_ascii(obj.query))
    except:
      return "Bad query"
    return "<table>%s</table>"%(''.join(["<tr><td>%s</td><td>%s</td></tr>"%i for i in sorted(params.items())]))
  query_list.allow_tags = True
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

from main.signals import *

try:
  from django.contrib.contenttypes.models import ContentType
  ContentType.__unicode__ = lambda self: "%s - %s"%(self.app_label,self.model)
  if settings.DEBUG:
    @admin.register(LogEntry)
    class LogEntryAdmin(admin.ModelAdmin):
      list_filter = ('content_type',)
      list_display = ('__unicode__','action_time','content_type','user')
      raw_id_fields = ('user',)
    ContentType._meta.ordering = ('model',)
    admin.site.register(ContentType)
except:
  pass
