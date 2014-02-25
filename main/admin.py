from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import *
from django import forms

from codrspace.admin import TaggedPhotoInline
from membership.models import UserMembership
admin.site.unregister(FlatPage)
admin.site.unregister(User)

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
  has_delete_permission = lambda self,request,obj: False
  model = UserMembership

class UserAdmin(UserAdmin):
  has_delete_permission = lambda self,request,obj: request.user.is_superuser
  inlines = [UserMembershipInline]

admin.site.register(FlatPage,FlatPageAdmin)
admin.site.register(User,UserAdmin)

from .signals import *
