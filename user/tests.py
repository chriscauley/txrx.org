from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core.mail import outbox

from main.test_utils import TXRXTestCase

class PasswordResetTestCase(TXRXTestCase):
  def test_inactive_user(self):
    """
    By default django won't reset passwords for non-active users.
    We'd rather activate the user first then reset password.
    """
    user = self.new_user()
    user.active = False
    user.save()
    self.client.post(reverse('password_reset'),{'email':user.email})
    self.check_subjects(['Password reset on example.com'])
    user = get_user_model().objects.get(id=user.id)
    self.assertTrue(user.is_active)
  def test_bad_email(self):
    """ If people try to reset password with a non-existant email, tell them they never registered """
    self.client.post(reverse('password_reset'),{'email':"email_DNE@example.com"})
    self.check_subjects(["Someone attempted a password reset for %s"%settings.SITE_NAME])
  def test_paypal_email(self):
    """ Since we allow paypal emails to be used for login, it should also work with password reset """
    user = self.new_user()
    user.paypal_email = "my_paypal_email@example.com"
    user.save()
    self.client.post(reverse('password_reset'),{'email':user.paypal_email})
    self.check_recipients([[user.paypal_email]])
  def test_inactive_login(self):
    user = self.new_user(password="password")
    user.is_active = False
    user.save()
    r = self.client.post(reverse('auth_login'),{'username': user.username, 'password': 'password'},follow=True)
    messages = r.context['messages']._get()[0]
    self.assertTrue("Your account is inactive" in messages[0].message)
    self.check_subjects(["Activate your account"])
