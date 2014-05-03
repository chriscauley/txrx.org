from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import *
from django.core.urlresolvers import reverse
from django import forms

from codrspace.admin import TaggedPhotoInline
from membership.models import UserMembership

from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.ipn.admin import PayPalIPNAdmin

admin.site.unregister(FlatPage)
admin.site.unregister(User)
admin.site.unregister(PayPalIPN)

TEMPLATE_CHOICES = (
  ('','HTML'),
  ('flatpages/markdown.html','MarkDown'),
  )

class FlatPageForm(forms.ModelForm):
  template_name = forms.CharField("Render As",help_text="",required=False)
  def __init__(self, *args, **kwargs):
    super(FlatPageForm, self).__init__(*args, **kwargs)
    self.fields['template_name'].widget = forms.Select(choices=TEMPLATE_CHOICES)
  class Meta:
    model = FlatPage

class FlatPageAdmin(FlatPageAdmin):
  form = FlatPageForm
  inlines = [TaggedPhotoInline]

class UserMembershipInline(admin.StackedInline):
  extra = 0
  has_add_permission = lambda self,request: False
  has_delete_permission = lambda self,*args: False
  model = UserMembership

class UserAdmin(UserAdmin):
  inlines = [UserMembershipInline]

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
    pass
  view_IPN.allow_tags = True

admin.site.register(FlatPage,FlatPageAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(PayPalIPN,CustomIPNAdmin)

from .signals import *
