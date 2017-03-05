from django.conf import settings
from django.core import mail
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.utils import timezone

from course.models import Course, Session, Room, Enrollment
from lablackey.contenttypes import get_contenttype
from main.test_utils import TXRXTestCase
from sms.models import SMSNumber
import sms

import datetime,random

#! TODO I know its bad to hardcode many of these variables
# for now they are marked with bad so that they can be removed when I figure out the test runner

def new_session(course):
    session = Session.objects.create(course=course,user_id=3) #! BAD
    session.classtime_set.get_or_create(
        start=timezone.now()+datetime.timedelta(random.randint(1,40)),
        end_time="12:00"
    )
    session = Session.objects.get(pk=session.pk)
    session.save()
    return session

class NotificationTestCase(TXRXTestCase):
    def setUp(self):
        super(NotificationTestCase,self).setUp()
        self.follow_url = reverse("notify_follow",args=["course.Course",self.course1.id])
        self.follow_url2 = reverse("notify_follow",args=["course.Course",self.course2.id])
    def test_flow(self):
        user = self.login("chriscauley",password="badpassword") #! BAD
        user.follow_set.all().delete() #! BAD

        # user follows the course
        self.client.get(self.follow_url)
        self.assertEqual(user.follow_set.all()[0].object_id,self.course1.id)

        # a new session is created
        session = new_session(self.course1)

        # user has a notification for the new session
        self.assertEqual(user.notification_set.filter(read__isnull=True).count(),1)
        notification = user.notification_set.all()[0]
        self.assertEqual(notification.target,session)
        call_command("notify_course")
        self.assertEqual(len(mail.outbox),1)
        self.assertEqual("New classes at %s"%settings.SITE_NAME,mail.outbox[0].subject)
        self.assertTrue("%s%s"%(settings.SITE_URL,session.get_absolute_url()) in mail.outbox[0].body)

        # user will not get emailed if management command runs again
        mail.outbox = []
        call_command("notify_course")
        self.assertEqual(len(mail.outbox),1)
        self.assertEqual(mail.outbox[0].body,"No new classes to notify anyone about :(")

        # user visits class page from email link notification is read
        self.client.get(session.get_absolute_url())
        self.assertEqual(user.notification_set.filter(read__isnull=True).count(),0)

        # user signs up for session, forcing unfollow on course
        Enrollment.objects.create(user=user,session=session)
        self.assertEqual(user.follow_set.all().count(),0)

    def test_edges(self):
        user = self.login("chriscauley",password="badpassword") #! BAD
        user.follow_set.all().delete() #! BAD

        # user follows two courses
        self.client.get(self.follow_url)
        self.client.get(self.follow_url2)
        self.assertEqual(
            sorted([f.object_id for f in user.follow_set.all()]),
            sorted([self.course1.id,self.course2.id])
        )

        # two sessions added for one course, one session added for the other
        session = new_session(self.course1)
        session2 = new_session(self.course2)
        session22 = new_session(self.course2)

        # management command sends one email to student, containing links to all three classes
        call_command("notify_course")
        self.assertEqual(len(mail.outbox),1)
        self.assertEqual("New classes at %s"%settings.SITE_NAME,mail.outbox[0].subject)
        for s in [session,session2,session22]:
            self.assertTrue("<%s%s>"%(settings.SITE_URL,s.get_absolute_url()) in mail.outbox[0].body)

        # user unfollows course via email link
        follow = user.follow_set.all()[0]
        self.client.get(reverse("notify_unfollow",args=[follow.id]))
        self.assertEqual(user.follow_set.all().count(),1)

        # refollow both (actually results in only 1 additional follow
        self.client.get(self.follow_url)
        self.client.get(self.follow_url2)
        self.assertEqual(user.follow_set.all().count(),2)

        # use the super unfollow
        self.client.get(reverse("unsubscribe",args=["notify_course",user.id]))
        self.assertEqual(user.follow_set.all().count(),0)

    def test_sms_preference(self):
        user = self.new_user()
        user_sms = self.new_user()
        # sign users up for class tomorrow
        Enrollment.objects.create(user=user,session=self.session1)
        Enrollment.objects.create(user=user_sms,session=self.session1)

        # set user_sms preference to text
        notifysettings = user_sms.notifysettings
        notifysettings.my_classes = 'sms'
        notifysettings.save()
        SMSNumber.objects.create(user=user_sms,number='1234567890')

        # run management command
        call_command('course_reminder')
        call_command('notify_course')

        # verify user received text and mail outbox is empty
        self.check_subjects(["You're teaching tomorrow at 1 p.m.","Class tomorrow!"])
        self.assertEqual("You have class tomorrow at TXRX Labs: course45 @ 1 p.m.",sms.outbox[0].body)
        self.assertEqual(len(sms.outbox),1)
        sms.outbox = []

        # run management command
        call_command('course_reminder')
        call_command('notify_course')

        self.check_subjects([])
        self.assertEqual(len(sms.outbox),0)
