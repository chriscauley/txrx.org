from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.db.models import Q
from django.test import TestCase

from membership.paypal_utils import get_course_query, paypal_post
from membership.models import Level

from course.models import Session, Course, ClassTime, Enrollment
from .utils import get_or_create_student
from lablackey.tests import check_subjects, check_recipients

import arrow

#stupid requests ssl error
import warnings
warnings.showwarning = lambda *x: None

def setUp(self):
  tomorrow = arrow.now().replace(days=1,hour=13,minute=00).datetime
  next_day = arrow.now().replace(days=2,hour=13,minute=00).datetime
  end = "14:00"

  # fee = 45 because it tests that discounts are including fractional dollars
  # Session 1 has class tomorrow and the next day from 1-2pm
  self.session1 = Session.objects.create(
    course=Course.objects.filter(active=True,fee=45).order_by("?")[0],
    user_id=1
  )
  ClassTime.objects.create(session=self.session1,start=tomorrow,end_time=end)
  ClassTime.objects.create(session=self.session1,start=next_day,end_time=end)

  # Session 2 has class day after tomorrow at the same time as session 1
  self.session2 = Session.objects.create(
    course=Course.objects.filter(active=True,fee__gt=0).order_by("?")[0],
    user_id=1
  )
  ClassTime.objects.create(session=self.session2,start=tomorrow.replace(hour=18),end_time="19:00")

  # conflict_session1 is the same time as session1. currently unused
  self.conflict_session1 = Session.objects.create(
    course=Course.objects.filter(active=True,fee__gt=0).order_by("?")[0],
    user_id=1
  )
  ClassTime.objects.create(session=self.conflict_session1,start=next_day,end_time=end)

class ListenersTest(TestCase):
  """This tests all possible purchases from paypal and to make sure prices line up.
  This uses artificial IPN data, not the actual IPN."""
  setUp = setUp
  def test_quantity(self):
    """
    Pay for a class with more than one quantity. Make sure enrollment and session.total students is correct
    Pay for a class that the user is already enrolled in. ibid.
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
    params = get_course_query(session=self.session1,quantities=[2],payer_email=email)
    paypal_post(self,params)

    enrollment = self.session1.enrollment_set.get()
    self.assertEqual(enrollment.quantity,2)
    self.assertEqual(enrollment.user,user)

    params = get_course_query(session=self.session1,quantities=[1],payer_email=email)
    paypal_post(self,params)

    enrollment = self.session1.enrollment_set.get()
    self.assertEqual(enrollment.quantity,3)
    self.assertEqual(enrollment.user,user)
  def test_discount(self):
    email = "prexistinguser@txrxlabs.com"
    get_user_model().objects.filter(email=email).delete()
    user = get_user_model().objects.create(
      username="preexistinguser",
      email=email
    )
    user.level = Level.objects.filter(discount_percentage=10)[0]
    user.save()
    params = get_course_query(session=self.session1,quantities=[1],payer_email=email)
    paypal_post(self,params)

    # The above generates an enrollment error because someone over paid
    self.assertTrue(check_subjects(["Enrollment Error","Course enrollment confirmation"]))

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
    self.assertTrue(check_subjects(["Course enrollment confirmation","New account information"]))
    for message in mail.outbox:
      self.assertEqual([email], message.recipients())

    # now test same address with another class
    mail.outbox = []
    params = get_course_query(session=self.session2,payer_email=email)
    paypal_post(self,params)
    self.assertTrue(check_subjects(["Course enrollment confirmation"]))
    for message in mail.outbox:
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

class NotifyTest(TestCase):
  setUp = setUp
  def test_course(self):
    #make sure students and instructors get an email
    i_email = 'instructor@txrxtesting.com'
    s_email = 'student@txrxtesting.com'
    s2_email = 'student2@txrxtesting.com'
    User = get_user_model()
    User.objects.filter(email__in=[i_email,s_email,s2_email]).delete()
    instructor, new = get_or_create_student(i_email,send_mail=False)
    instructor.is_staff = True
    instructor.save()

    self.session1.user = instructor
    self.session2.user = instructor
    self.session1.save()
    self.session2.save()

    # enroll student in 1 class
    student, new = get_or_create_student(s_email,send_mail=False)
    Enrollment.objects.create(user=student,session=self.session1)

    # enroll student2 in 2 classes
    student2,new = get_or_create_student(s2_email,send_mail=False)
    Enrollment.objects.create(user=student,session=self.session1)

    # send out reminders and check that they went out
    call_command("course_reminder")
    subjects = [u"You're teaching tomorrow at 1 p.m.", u'Class tomorrow!', 'Course reminders']
    recipients = [[i_email], [s_email], ['chris@lablackey.com']]
    self.assertTrue(check_subjects(subjects))
    self.assertTrue(check_recipients(recipients))

    # send out reminders again. Make sure none went out
    mail.outbox = []
    call_command("course_reminder")
    self.assertTrue(check_subjects([]))
    self.assertTrue(check_recipients([]))
    
