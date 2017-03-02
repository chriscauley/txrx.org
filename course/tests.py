from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.db.models import Q

from membership.paypal_utils import get_course_query, paypal_post

from course.models import Enrollment
from main.test_utils import TXRXTestCase
from drop.models import Cart

#stupid requests ssl error
import warnings
warnings.showwarning = lambda *x: None

class ListenersTest(TXRXTestCase):
  """This tests all possible purchases from paypal and to make sure prices line up.
  This uses artificial IPN data, not the actual IPN."""
  def test_quantity(self):
    """
    Pay for a class with more than one quantity. Make sure enrollment and session.total students is correct
    Pay for a class that the user is already enrolled in. ibid.
    """
    email = "preexisting@example.com"
    paypal_email = "different@example.com"
    user = self.new_user(username=email)
    self.login(user)

    # create cart with cart_item
    invoice = self.add_to_cart(self.session1.sessionproduct,2)

    # fake the IPN
    params = get_course_query(session=self.session1,quantities=[2],payer_email=email,invoice=invoice)
    paypal_post(self,params)

    # Did it work?
    enrollment = self.session1.enrollment_set.get()
    self.assertEqual(enrollment.quantity,2)
    self.assertEqual(enrollment.user,user)

    # Lets do it again with 1 enrollment...
    invoice = self.add_to_cart(self.session1.sessionproduct)
    params = get_course_query(session=self.session1,quantities=[1],payer_email=email,invoice=invoice)
    paypal_post(self,params)

    # ...and see if the enrollment increased
    enrollment = self.session1.enrollment_set.get()
    self.assertEqual(enrollment.quantity,3)
    self.assertEqual(enrollment.user,user)
  def test_discount(self):
    from paypal.standard.ipn.models import PayPalIPN
    email = "prexistinguser@txrxlabs.com"
    get_user_model().objects.filter(email=email).delete()
    user = get_user_model().objects.create(
      username="preexistinguser",
      email=email
    )
    user.level = self.level10
    user.save()
    self.login(user)

    # create cart with cart_item
    invoice = self.add_to_cart(self.session1.sessionproduct)

    params = get_course_query(session=self.session1,quantities=[1],payer_email=email,invoice=invoice)
    paypal_post(self,params)

    # The above generates an enrollment error because someone over paid
    self.check_subjects(["Course enrollment confirmation"])

class UtilsTest(TXRXTestCase):
  """ Test the following parameters of the get_or_create_student functions.
  paypal_email - should return correct student
  u_id - should return user.id = u_id or user.email = u_id
  subscr_id - tested in membership.tests
  """
  def test_paypal_email(self):
    email = "ihasnoemail@txrxlabstest.com"
    get_user_model().objects.filter(email=email).delete()

    invoice = self.add_to_cart(self.session1.sessionproduct)
    # test first with no account
    params = get_course_query(session=self.session1,payer_email=email,invoice=invoice)
    paypal_post(self,params)

    # make sure only these two emails were sent to only that one address
    self.check_subjects(["Course enrollment confirmation","New account information"])
    for message in mail.outbox:
      self.assertEqual([email], message.recipients())

    # now test same address with another class
    mail.outbox = []
    invoice = self.add_to_cart(self.session2.sessionproduct,1)
    params = get_course_query(session=self.session2,payer_email=email,invoice=invoice)
    paypal_post(self,params)
    self.check_subjects(["Course enrollment confirmation"])
    for message in mail.outbox:
      self.assertEqual([email], message.recipients())

    # make sure a new account is not created and that the enrollments are right
    self.assertEqual(get_user_model().objects.filter(email=email).count(),1)
    # Note these next two lines use "get" because more than one enrollment throws an error.
    self.assertEqual(self.session1.enrollment_set.get().user.email,email)
    self.assertEqual(self.session2.enrollment_set.get().user.email,email)

  def test_uid(self):
    username = "preexistinguser"
    paypal_email = "different@txrxlabs.org"
    user = self.new_user(username)
    self.login(user)

    # buy a class while logged in
    invoice = self.add_to_cart(self.session1.sessionproduct)
    params = get_course_query(session=self.session1,payer_email=paypal_email,custom=user.pk,invoice=invoice)
    paypal_post(self,params)

    # no new counts should have been created and the user now has enrollments/paypal_email
    user = get_user_model().objects.get(email=user.email) # refresh instance
    q1 = Q(email__in=[user.email,paypal_email])
    q2 = Q(paypal_email__in=[user.email,paypal_email])
    self.assertEqual(get_user_model().objects.filter(q1|q2).count(),1)
    self.assertEqual(self.session1.enrollment_set.get(user=user).quantity,1)
    self.assertEqual(user.paypal_email,paypal_email)

class NotifyTest(TXRXTestCase):
  def test_course(self):
    # enroll student in 1 class
    Enrollment.objects.create(user=self.student1,session=self.session1)

    # enroll student2 in 2 classes
    Enrollment.objects.create(user=self.student2,session=self.session1)
    Enrollment.objects.create(user=self.student2,session=self.session2)

    # send out reminders and check that they went out
    call_command("course_reminder")
    call_command("notify_course")
    subjects = [
      u'Class tomorrow!', # student1
      u'2 classes tomorrow!', # student2
      u"You're teaching tomorrow at 1 p.m." # teacher
    ]
    recipients = [[u.email] for u in [self.student1, self.student2, self.teacher]]
    self.check_subjects(subjects)
    self.check_recipients(recipients)

    # send out reminders again. Make sure none went out
    mail.outbox = []
    call_command("course_reminder")
    call_command("notify_course")
    self.check_subjects([])
    self.check_recipients([])
