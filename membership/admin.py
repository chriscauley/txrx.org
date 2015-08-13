from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django import forms

from models import (MembershipGroup, Membership, Feature, MembershipFeature, UserMembership, MembershipChange,
                    MembershipProduct, MeetingMinutes, Proposal, Officer)

from db.admin import RawMixin
from db.forms import StaffMemberForm

class MembershipFeatureInline(RawMixin,admin.TabularInline):
  extra = 0
  raw_id_fields = ('membership','feature')
  model = MembershipFeature

class MembershipProductInline(admin.TabularInline):
  extra = 0
  model = MembershipProduct
  exclude = ('slug',)

class MembershipAdmin(admin.ModelAdmin):
  list_display = ("name","order")
  list_editable = ("order",)
  inlines = (MembershipFeatureInline, MembershipProductInline)

class MembershipChangeInline(admin.TabularInline):
  model = MembershipChange
  extra = 1
  exclude = ('paypalipn','transaction_id')
  readonly_fields = ('payment_method','ipn_link')
  def ipn_link(self,obj=None):
    if not (obj and obj.pk):
      return ""
    if obj.paypalipn:
      return "<a href='/admin/ipn/paypalipn/%s/'>%s</a>"%(obj.paypalipn.pk,obj.transaction_id)
    return obj.transaction_id
  ipn_link.allow_tags = True
  has_delete_permission = lambda self, request, obj=None: settings.DEBUG

class UserMembershipInline(admin.StackedInline):
  list_display = ("__unicode__",'photo')
  list_editable = ('photo',)
  list_filter = ('user__is_staff',)
  search_fields = ('user__email','user__username','paypal_email')
  readonly_fields = ('api_key','start','end')
  raw_id_fields = ('photo',)
  model = UserMembership

class ProposalInline(admin.StackedInline):
  model = Proposal
  fields = ('order','title','user','original','ammended')
  extra = 0

class MeetingMinutesForm(forms.ModelForm):
  User = get_user_model()
  kwargs = dict(widget=forms.CheckboxSelectMultiple(),required=False)
  _q = User.objects.filter(usermembership__voting_rights=True,usermembership__suspended=False)
  voters_present = forms.ModelMultipleChoiceField(queryset=_q,**kwargs)
  _q = User.objects.filter(usermembership__voting_rights=True,usermembership__suspended=True)
  kwargs = dict(widget=forms.CheckboxSelectMultiple(),required=False)
  inactive_present = forms.ModelMultipleChoiceField(queryset=_q,**kwargs)
  class Meta:
    model = MeetingMinutes
    exclude = ()

class MeetingMinutesAdmin(admin.ModelAdmin):
  form = MeetingMinutesForm
  inlines = [ProposalInline]
  fields = ('date','content',('voters_present','inactive_present'),'nonvoters_present')
  filter_horizontal = ('nonvoters_present',)

class OfficerAdmin(admin.ModelAdmin):
  form = StaffMemberForm

admin.site.register(Membership,MembershipAdmin)
admin.site.register(MeetingMinutes,MeetingMinutesAdmin)
admin.site.register(Officer,OfficerAdmin)
admin.site.register(Feature)
admin.site.register(MembershipGroup)
