from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User
from .forms import UserChangeForm, CustomUserCreationForm

class UserAdmin(UserAdmin):
  fieldsets = (
    (None, {'fields': ('username', 'email', 'password')}),
    (_('Personal info'), {'fields': ('first_name', 'last_name')}),
    (_('Permissions'),
     {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
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
  list_display = ('username', 'first_name', 'last_name', 'is_staff')
  search_fields = ('username', 'email', 'first_name', 'last_name')
  ordering = ('username',)
  readonly_fields = ('last_login','date_joined')

admin.site.register(User, UserAdmin)
