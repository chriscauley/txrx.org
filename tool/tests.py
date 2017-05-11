#this test never really got implemented. Going to replace it with new expires on criteria

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from course.models import Session
from membership.models import Level, Flag
from membership.paypal_utils import get_membership_query, paypal_post

import datetime

class SafetyTest(TestCase):
  """ Tests for tool.management.commands.check_permissions """
  def setUp(self):
    # create user and give him a hacker membership, this should generate a safety criterion
    self.email = 'safetytester@txrxtesting.com'
    level = Level.objects.get(name="Hacker")
    product = level.product_set.all()[0]
    data = get_membership_query(product=product,payer_email=self.email)
    paypal_post(self,data)

    #! TODO this is bad for now should not need to delete an entire set of courses just for this
    Session.objects.filter(course_id=settings.SAFETY_ID).delete()
    Flag.objects.all().delete()
    self.session = Session.objects.create(course_id=settings.SAFETY_ID,user_id=1)

  def test_create_temporary_criterion(self):
    now = datetime.datetime.now()
    user = get_user_model().objects.get(email=self.email)
    criterion = user.usercriterion_set.get()
    self.assertEqual(user.usercriterion_set.count(),1)
    self.assertEqual(user.usercriterion_set.all()[0].content_type.model,"subscription")

    # user looses his safety pass at the next session
    criterion.created = now - datetime.timedelta(45)
    criterion.save()
    self.session.first_date = now + datetime.timedelta(7.5)
    self.session.save()
    self.call_command("check_permissions")
    
