from django.contrib import admin
from models import Membership, Feature, UserMembership, MembershipRate, MeetingMinutes, Proposal

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

class ProposalInline(admin.StackedInline):
  model = Proposal
  fields = (('order','title'),'original','ammended')
  extra = 0

class MeetingMinutesAdmin(admin.ModelAdmin):
  inlines = [ProposalInline]

admin.site.register(Membership,MembershipAdmin)
admin.site.register(UserMembership,UserMembershipAdmin)
admin.site.register(MeetingMinutes,MeetingMinutesAdmin)
