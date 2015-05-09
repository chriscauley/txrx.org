from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class CustomUserCreationForm(UserCreationForm):
  #! These two fields methods are identical to the original but necessary because
  #! original UserCreationForm uses django.contrib.auth.models.User instead of
  #! get_user_model. Probably fixed in 1.7
  def clean_username(self):
    # Since User.username is unique, this check is redundant,
    # but it sets a nicer error message than the ORM. See #13147.
    username = self.cleaned_data["username"]
    try:
      User._default_manager.get(username=username)
    except User.DoesNotExist:
      return username
    raise forms.ValidationError(self.error_messages['duplicate_username'])

  def save(self, commit=True):
    user = super(UserCreationForm, self).save(commit=False)
    user.set_password(self.cleaned_data["password1"])
    if commit:
      user.save()
    return user
  class Meta:
    model = User
    fields = ("username","email",)

class UserChangeForm(UserChangeForm):
  class Meta:
    model = User
    exclude = ('',)
