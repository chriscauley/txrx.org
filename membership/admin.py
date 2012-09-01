from django.contrib import admin
from models import Membership, Feature, Profile

class FeatureInline(admin.TabularInline):
    extra = 0
    model = Feature

class MembershipAdmin(admin.ModelAdmin):
    list_display = ("name","order")
    list_editable = ("order",)
    inlines = (FeatureInline,)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("__unicode__",'photo')
    list_editable = ('photo',)
    exclude = ("ghandle",) #gmail email address from ProfileModel


admin.site.register(Membership,MembershipAdmin)
admin.site.register(Profile,ProfileAdmin)
