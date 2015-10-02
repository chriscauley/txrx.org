from django.contrib.auth import get_user_model
from django.core import mail
from django.db.models import Q
from django.test import TestCase

from membership.paypal_utils import get_course_query, paypal_post

from course.models import Session, Course, ClassTime, Enrollment

import datetime

#stupid requests ssl error
import warnings
warnings.showwarning = lambda *x: None

def setUp(self):
  self.session1 = Session.objects.create(
    course=Course.objects.filter(active=True).order_by("?")[0],
    user_id=1
  )
  ClassTime.objects.create(
    session=self.session1,
    start=datetime.datetime(2020,1,1,12),
    end_time="12:00"
  )
  self.session2 = Session.objects.create(
    course=Course.objects.filter(active=True).order_by("?")[0],
    user_id=1
  )
  ClassTime.objects.create(
    session=self.session2,
    start=datetime.datetime(2021,1,1,12),
    end_time="12:00"
  )

class ListenersTest(TestCase):
  """This tests all possible purchases from paypal and to make sure prices line up.
  This uses artificial IPN data, not the actual IPN."""
  setUp = setUp
  def test_annonymous_purchase(self):
    """
    Pay for a class with a non-existent user. Verify price, enrollment, email, and new account.
    Then test the same user and make sure a second account was not created.
    """
    pass
  def test_discounts(self):
    """
    Pay for a class with a membership that has a discount.
    Make sure that the price was correct, the user is enrolled, and no new accounts were created.
    """
    pass
  def test_quantity(self):
    """
    Pay for a class with more than one quantity. Make sure enrollment and session.total students is correct
    Pay for a class that the user is alread enrolled in. ibid.
    """
    email = "preexistinguser@txrxlabstest.com"
    paypal_email = "adifferentemail@txrxlabstest.com"
    q1 = Q(email__in=[email,paypal_email])
    q2 = Q(usermembership__paypal_email__in=[email,paypal_email])
    get_user_model().objects.filter(q1|q2).delete()
    user = get_user_model().objects.create(
      username="preexisinguser",
      email=email
    )

del ListenersTest

class UtilsTest(TestCase):
  """ Test the following parameters of the get_or_create_student functions.
  paypal_email - should return correct student
  u_id - should return user.id = u_id or user.email = u_id
  subscr_id - tested in membership.tests
  """
  setUp = setUp
  def test_paypal_email(self):
    email = "ihasnoemail@txrxlabstest.com"
    get_user_model().objects.filter(email=email).delete()
    # test first with no account
    params = get_course_query(session=self.session1,payer_email=email)
    paypal_post(self,params)

    # make sure only these two emails were sent to only that one address
    subjects = ["[TXRX] Course enrollment confirmation","[TXRX] New account information"]
    for message in mail.outbox:
      self.assertTrue(message.subject in subjects)
      self.assertEqual([email], message.recipients())

    # now test same address with another class
    mail.outbox = []
    params = get_course_query(session=self.session2,payer_email=email)
    paypal_post(self,params)
    for message in mail.outbox:
      self.assertEqual(message.subject,subjects[0])
      self.assertEqual([email], message.recipients())

    # make sure a new account is not created and that the enrollments are right
    self.assertEqual(get_user_model().objects.filter(email=email).count(),1)
    # Note these next two lines use "get" because more than one enrollment throws an error.
    self.assertEqual(Enrollment.objects.get(session=self.session1).user.email,email)
    self.assertEqual(Enrollment.objects.get(session=self.session2).user.email,email)

  def test_uid(self):
    email = "preexistinguser@txrxlabstest.com"
    paypal_email = "adifferentemail@txrxlabstest.com"
    q1 = Q(email__in=[email,paypal_email])
    q2 = Q(usermembership__paypal_email__in=[email,paypal_email])
    get_user_model().objects.filter(q1|q2).delete()
    user = get_user_model().objects.create(
      username="preexisinguser",
      email=email
    )

    # buy a class while logged in
    params = get_course_query(session=self.session1,payer_email=paypal_email,custom=user.pk)
    paypal_post(self,params)

    # no new counts should have been created and the user now has enrollments/paypal_email
    user = get_user_model().objects.get(email=email) # refresh instance
    self.assertEqual(get_user_model().objects.filter(q1|q2).count(),1)
    self.assertEqual(self.session1.enrollment_set.get(user=user).quantity,1)
    self.assertEqual(user.usermembership.paypal_email,paypal_email)
