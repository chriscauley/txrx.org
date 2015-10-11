from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User
from membership.admin import UserMembershipInline, SubscriptionInline
from .forms import UserChangeForm, CustomUserCreationForm

class UserAdmin(UserAdmin):
  fieldsets = (
    (None, {'fields': ('username', 'email', 'password', ('first_name', 'last_name'),('rfid','level'))}),
    (_('Permissions'),
     {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_toolmaster', 'groups')}),
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
  search_fields = ('username', 'email', 'first_name', 'last_name','usermembership__paypal_email')
  ordering = ('username',)
  readonly_fields = ('last_login','date_joined','level')
  inlines = [UserMembershipInline, SubscriptionInline]

admin.site.register(User, UserAdmin)
