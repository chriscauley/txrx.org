from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import User

class PasswordResetForm(PasswordResetForm):
  def get_users(self,email):
    """
    Searches keyword search instead of filter(email=email)
    Also doesn't care about whether or not users are active
    """
    return User.objects.keyword_search(email)
  def save(self, domain_override=None,
           subject_template_name='registration/password_reset_subject.txt',
           email_template_name='registration/password_reset_email.html',
           use_https=False, token_generator=default_token_generator,
           from_email=None, request=None, html_email_template_name=None,
           extra_email_context=None):
    """
    Generates a one-use only link for resetting password and sends to the user.
    """
    email = self.cleaned_data["email"]
    if not domain_override:
      current_site = get_current_site(request)
      site_name = current_site.name
      domain = current_site.domain
    else:
      site_name = domain = domain_override
    for user in self.get_users(email):
      context = {
        'email': email,
        'domain': domain,
        'site_name': site_name,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': token_generator.make_token(user),
        'protocol': 'https' if use_https else 'http',
      }
      if extra_email_context is not None:
        context.update(extra_email_context)
      self.send_mail(subject_template_name, email_template_name,
                     context, from_email, email,
                     html_email_template_name=html_email_template_name)

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
