from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.utils import timezone

from course.models import Course, Session, Room, Enrollment
from lablackey.contenttypes import get_contenttype
from main.test_utils import TXRXTestCase
from lablackey.sms.models import SMSNumber
from lablackey import sms

import datetime,random

def new_session(course,teacher):
    session = Session.objects.create(course=course,user=teacher)
    start = datetime.datetime.now().replace(hour=13)
    session.classtime_set.get_or_create(
        start=start+datetime.timedelta(random.randint(1,60)),
        end_time="12:00"
    )
    session = Session.objects.get(pk=session.pk)
    session.save()
    return session

class NotificationTestCase(TXRXTestCase):
    def setUp(self):
        super(NotificationTestCase,self).setUp()
        # clear any backlog made by the above super
        self.call_command("notify_course")
        mail.outbox = []
        self.follow_url = reverse("notify_follow",args=["course.Course",self.course1.id])
        self.follow_url2 = reverse("notify_follow",args=["course.Course",self.course2.id])
    def test_flow(self):
        user = self.new_user()
        self.login(user)

        # user follows the course
        self.client.get(self.follow_url)
        self.assertEqual(user.follow_set.all()[0].object_id,self.course1.id)

        session1 = new_session(self.course1,self.teacher)

        # user has a notification for the new session
        self.assertEqual(user.notification_set.filter(read__isnull=True).count(),1)
        notification = user.notification_set.all()[0]
        self.assertEqual(notification.target,session1)
        self.call_command("notify_course")
        self.assertEqual(len(mail.outbox),1)
        self.assertEqual("New classes at %s"%settings.SITE_NAME,mail.outbox[0].subject)
        self.assertTrue("%s%s"%(settings.SITE_URL,session1.get_absolute_url()) in mail.outbox[0].body)

        # user will not get emailed if management command runs again
        mail.outbox = []
        self.call_command("notify_course")
        self.assertEqual(len(mail.outbox),0)

        # user visits class page from email link notification is read
        self.client.get(session1.get_absolute_url())
        self.assertEqual(user.notification_set.filter(read__isnull=True).count(),0)

        # user signs up for session, forcing unfollow on course
        Enrollment.objects.create(user=user,session=session1)
        self.assertEqual(user.follow_set.all().count(),0)

        # follow again but this time with sms
        self.client.get(self.follow_url)
        self.assertEqual(user.follow_set.all()[0].object_id,self.course1.id)

        notifysettings = user.notifysettings
        notifysettings.new_sessions = "sms"
        notifysettings.save()
        SMSNumber.objects.get_or_create(user=user,number='1234567890',verified=datetime.datetime.now())

        session1a = new_session(self.course1,self.teacher)
        # user has a notification for the new session
        self.assertEqual(user.notification_set.filter(read__isnull=True).count(),1)
        notification = user.notification_set.all()[0]
        self.assertEqual(notification.target,session1a)
        mail.outbox = []
        sms.outbox = []
        self.call_command("notify_course")
        self.assertEqual(len(mail.outbox),0)
        m = 'There a new session of course45 at TXRX Labs. Visit %s to find out more'
        self.assertEqual(sms.outbox[0].body,m%settings.NOTIFY_URL)

    def test_edges(self):
        user = self.new_user()
        self.login(user)

        # user follows two courses
        self.client.get(self.follow_url)
        self.client.get(self.follow_url2)
        self.assertEqual(
            sorted([f.object_id for f in user.follow_set.all()]),
            sorted([self.course1.id,self.course2.id])
        )

        session1 = new_session(self.course1,self.teacher)
        session2 = new_session(self.course2,self.teacher)
        session22 = new_session(self.course2,self.teacher)
        # management command sends one email to student, containing links to all three classes
        self.call_command("notify_course")
        self.assertEqual(len(mail.outbox),1)
        self.assertEqual("New classes at %s"%settings.SITE_NAME,mail.outbox[0].subject)
        for s in [session1,session2,session22]:
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
        sms.outbox = []
        self.call_command('course_reminder')
        self.call_command('notify_course')

        # verify user received text and mail outbox is empty
        self.check_subjects(["You're teaching tomorrow at 1 p.m.","Class tomorrow!"])
        self.assertEqual("You have class tomorrow at TXRX Labs: course45 @ 1 p.m.",sms.outbox[0].body)
        self.assertEqual(len(sms.outbox),1)
        sms.outbox = []

        # run management command
        self.call_command('course_reminder')
        self.call_command('notify_course')

        self.check_subjects([])
        self.assertEqual(len(sms.outbox),0)
