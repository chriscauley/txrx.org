from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeForm, CustomUserCreationForm
from .models import User, UserNote, UserCheckin

from course.admin import EnrollmentInline, CourseEnrollmentInline
from membership.admin import UserMembershipInline, SubscriptionInline, SubscriptionBuddyInline
from rfid.models import RFID

class UserNoteInline(admin.TabularInline):
  model = UserNote
  extra = 0
  readonly_fields = ("added",)

class RFIDInline(admin.TabularInline):
  model = RFID
  extra = 0

class WeakSubscriptionBuddyInline(SubscriptionBuddyInline):
  has_add_permission = lambda self, request: False
  readonly_fields = ("subscription","level_override","paid_until")

@admin.register(User)
class UserAdmin(UserAdmin):
  fieldsets = (
    (None, {'fields': (
      'username', 'password',
      ('email','paypal_email'),
      ('first_name', 'last_name'),
      'level',
      ('id_photo_date','headshot')
    )}),
    (_('Permissions'),
     {'fields': ('is_active', 'is_volunteer', 'is_staff', 'is_superuser',
                 'is_toolmaster', 'is_gatekeeper','is_shopkeeper', 'groups')}),
    (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('username', 'email', 'password1', 'password2')}
    ),
  )
  form = UserChangeForm
  add_form = CustomUserCreationForm
  list_display = ('username', 'get_full_name', 'is_staff','_enrollments')
  def _enrollments(self,obj):
    return "<br/>".join(unicode(e.session) for e in obj.enrollment_set.all())
  _enrollments.allow_tags = True
  search_fields = ('username', 'email', 'first_name', 'last_name','paypal_email')
  ordering = ('username',)
  readonly_fields = ('last_login','date_joined','level')
  inlines = [UserMembershipInline, RFIDInline, UserNoteInline, SubscriptionInline, WeakSubscriptionBuddyInline, EnrollmentInline,
             CourseEnrollmentInline]
  list_filter = list(UserAdmin.list_filter) + ['usermembership__voting_rights','date_joined','is_volunteer']

@admin.register(UserCheckin)
class UserCheckinAdmin(admin.ModelAdmin):
  readonly_fields = ("user","time_in","time_out","content_type","object_id","content_object")
  list_display = ("user","time_in","time_out","content_object")
