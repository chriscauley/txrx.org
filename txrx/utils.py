from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm

def cached_method (target):
  def wrapper(*args, **kwargs):
    obj = args[0]
    name = '_' + target.__name__

    if not hasattr(obj, name):
      value = target(*args, **kwargs)
      setattr(obj, name, value)

    return getattr(obj, name)
  
  return wrapper

def reset_password(user,
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt'):
  form = PasswordResetForm({'email':user.email})
  if form.is_valid():
    form.save(
      subject_template_name=subject_template_name,
      email_template_name=email_template_name)
    
  else:
    print form.errorsform.save(email_template_name=email_template_name)
