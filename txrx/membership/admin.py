from django.contrib import admin
from models import Membership, Feature, Profile

class FeatureInline(admin.TabularInline):
    model = Feature

class MembershipAdmin(admin.ModelAdmin):
    list_display = ("name","order")
    list_editable = ("order",)
    inlines = (FeatureInline,)

admin.site.register(Membership,MembershipAdmin)
admin.site.register(Profile)
