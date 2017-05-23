from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.core.urlresolvers import reverse
from django import forms
from django.http import QueryDict

from media.admin import TaggedPhotoInline
from membership.models import UserMembership

from lablackey.utils import latin1_to_ascii
from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.ipn.admin import PayPalIPNAdmin

admin.site.unregister(PayPalIPN)

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

admin.site.register(PayPalIPN,CustomIPNAdmin)

from main.signals import *

from django.contrib.contenttypes.models import ContentType
ContentType.__unicode__ = lambda self: "%s - %s"%(self.app_label,self.model)
ContentType._meta.ordering = ('app_label',)
try:
  if settings.DEBUG:
    @admin.register(LogEntry)
    class LogEntryAdmin(admin.ModelAdmin):
      list_filter = ('content_type',)
      list_display = ('__unicode__','action_time','content_type','user')
      raw_id_fields = ('user',)
    admin.site.register(ContentType)
except:
  pass
