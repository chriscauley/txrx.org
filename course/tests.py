from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.test import TestCase, Client

from membership.paypal_utils import get_course_query, paypal_post
from membership.models import Level

from course.models import Session, Course, ClassTime, Enrollment
from .utils import get_or_create_student
from geo.tests import setUp as geo_setUp
from lablackey.tests import check_subjects, check_recipients
from drop.test_utils import DropTestCase
from drop.models import Cart

import arrow

#stupid requests ssl error
import warnings
warnings.showwarning = lambda *x: None

def membership_setUp(self):
  defaults = {
    'name': 'foo',
    'order': 1
  }
  Level.objects.get_or_create(id=settings.DEFAULT_MEMBERSHIP_LEVEL,defaults=defaults)
  Level.objects.get_or_create(name="discounted",discount_percentage=10,order=999)

def setUp(self):
  tomorrow = arrow.now().replace(days=1,hour=13,minute=00).datetime
  next_day = arrow.now().replace(days=2,hour=13,minute=00).datetime
  end = "14:00"
  geo_setUp(self)
  membership_setUp(self)

  self.course1 = Course.objects.create(
    name="foo",
    active=True,
    fee=45,
    room=self.room,
    no_conflict=True,
  )

  self.course2 = Course.objects.create(
    name="bap",
    active=True,
    fee=50,
    room=self.room,
  )

  self.teacher = self.new_user()
  self.student1 = self.new_user()
  self.student2 = self.new_user()
  # fee = 45 because it tests that discounts are including fractional dollars
  # Session 1 has class tomorrow and the next day from 1-2pm
  self.session1 = Session.objects.create(course=self.course1,user=self.teacher)
  self.session1.save()
  ClassTime.objects.create(session=self.session1,start=tomorrow,end_time=end)
  ClassTime.objects.create(session=self.session1,start=next_day,end_time=end)
  self.session1 = Session.objects.get(pk=self.session1.pk)

  # Session 2 has class day after tomorrow at the same time as session 1
  self.session2 = Session.objects.create(course=self.course2,user=self.teacher)
  ClassTime.objects.create(session=self.session2,start=tomorrow.replace(hour=18),end_time="19:00")
  self.session2.save()

  # # conflict_session1 is the same time as session1. currently unused
  # self.conflict_session1 = Session.objects.create(
  #   course=Course.objects.filter(active=True,fee__gt=0).order_by("?")[0],
  #   user_id=1
  # )
  # ClassTime.objects.create(session=self.conflict_session1,start=next_day,end_time=end)

class ListenersTest(DropTestCase):
  """This tests all possible purchases from paypal and to make sure prices line up.
  This uses artificial IPN data, not the actual IPN."""
  setUp = setUp
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
    user.level = Level.objects.filter(discount_percentage=10)[0]
    user.save()
    client = Client()

    #login user
    client.post(reverse('login'),{'username': email,'password': email})

    # create cart with cart_item
    invoice = self.add_to_cart(self.session1.sessionproduct)

    params = get_course_query(session=self.session1,quantities=[1],payer_email=email,invoice=invoice)
    paypal_post(self,params)

    # The above generates an enrollment error because someone over paid
    self.check_subjects(["Course enrollment confirmation"])

class UtilsTest(DropTestCase):
  """ Test the following parameters of the get_or_create_student functions.
  paypal_email - should return correct student
  u_id - should return user.id = u_id or user.email = u_id
  subscr_id - tested in membership.tests
  """
  setUp = setUp
  def test_paypal_email(self):
    email = "ihasnoemail@txrxlabstest.com"
    get_user_model().objects.filter(email=email).delete()
    client = Client()

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
    self.assertEqual(Enrollment.objects.get(session=self.session1).user.email,email)
    self.assertEqual(Enrollment.objects.get(session=self.session2).user.email,email)

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

from lablackey.tests import ClientTestCase

class NotifyTest(ClientTestCase):
  setUp = setUp
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
