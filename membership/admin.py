from django.contrib import admin
from django.contrib.auth.models import User
from django import forms

from models import Membership, Feature, UserMembership, MembershipRate, MeetingMinutes, Proposal, Officer

from db.forms import StaffMemberForm

class FeatureInline(admin.TabularInline):
  extra = 0
  model = Feature

class MembershipRateInline(admin.TabularInline):
  extra = 0
  model = MembershipRate

class MembershipAdmin(admin.ModelAdmin):
  list_display = ("name","order")
  list_editable = ("order",)
  inlines = (FeatureInline,MembershipRateInline)

class UserMembershipAdmin(admin.ModelAdmin):
  list_display = ("__unicode__",'photo')
  list_editable = ('photo',)
  list_filter = ('user__is_staff',)
  search_fields = ('user__email','user__username','paypal_email')

class ProposalInline(admin.StackedInline):
  model = Proposal
  fields = (('order','title','user'),'original','ammended')
  extra = 0

class MeetingMinutesForm(forms.ModelForm):
  kwargs = dict(widget=forms.CheckboxSelectMultiple(),required=False)
  _q = User.objects.filter(usermembership__voting_rights=True,usermembership__suspended=False)
  voters_present = forms.ModelMultipleChoiceField(queryset=_q,**kwargs)
  _q = User.objects.filter(usermembership__voting_rights=True,usermembership__suspended=True)
  kwargs = dict(widget=forms.CheckboxSelectMultiple(),required=False)
  inactive_present = forms.ModelMultipleChoiceField(queryset=_q,**kwargs)
  class Meta:
    model = MeetingMinutes

class MeetingMinutesAdmin(admin.ModelAdmin):
  form = MeetingMinutesForm
  inlines = [ProposalInline]
  fields = ('date','content',('voters_present','inactive_present'),'nonvoters_present')
  filter_horizontal = ('nonvoters_present',)

class OfficerAdmin(admin.ModelAdmin):
  form = StaffMemberForm

admin.site.register(Membership,MembershipAdmin)
admin.site.register(UserMembership,UserMembershipAdmin)
admin.site.register(MeetingMinutes,MeetingMinutesAdmin)
admin.site.register(Officer,OfficerAdmin)
