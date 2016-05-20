from django.conf import settings
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(object):
  def authenticate(self, username=None, password=None):
    user = get_user_model().objects.get_from_anything(username)
    if user and user.check_password(password):
      return user
    return None

  def get_user(self, user_id):
    User = get_user_model()
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None
