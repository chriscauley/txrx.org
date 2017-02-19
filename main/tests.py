from django.test import TestCase, Client
from django.core.management import call_command
from django.core import mail

from lablackey.tests import check_subjects
from event.models import Event, EventOccurrence

import datetime, decimal

class ManagementCommands(TestCase):
  def setUp(self):
    self.now = datetime.datetime.now()
    self.in_an_hour = (self.now + datetime.timedelta(0,60*60)).time()
    self.tomorrow = self.now + datetime.timedelta(1)

  def test_repeat_events(self):
    Event.objects.filter(name="monkey").delete()
    e = Event.objects.create(name="monkey",repeat="month-number")
    eo = EventOccurrence.objects.create(start=self.tomorrow,end_time=self.in_an_hour,event=e)
    call_command("repeat_events")
    self.assertEqual(e.eventoccurrence_set.count(),5)
    subjects = [m.subject for m in mail.outbox]
    self.assertTrue(check_subjects([]))

  def test_evaluation_reminder(self):
    call_command("evaluation_reminder")
  def test_recalculate_subscriptions(self):
    call_command("recalculate_subscriptions")

  # done in course.tests
  #def test_course_reminder(self):
  #  call_command("course_reminder")

  def test_notify_course(self):
    call_command("notify_course")
  def test_reset_classes(self):
    call_command("reset_classes")

class TouchAllTheThings(TestCase):
  def test_no_login(self):
    urls = [
      '/',
      '/classes/',
      '/event/',
      '/thing/'
    ]
    client = Client()
    for u in urls:
      response = client.get(u)
      self.assertEqual(response.status_code,200)
    self.assertEqual(client.get('/nosuchpageexistsoreverexisted/').status_code,404)

from lablackey.tests import ClientTestCase
from membership.models import Status
from drop.models import OrderItem, Order

def get_data(**kwargs):
    data = {
      'metric': 'line_total',
      'product_types': 214,
      'time_period': 90,
      'resolution': 1
    }
    data.update(**kwargs)
    return data

class DashboardTest(ClientTestCase):
  """
  Test that the data coming out of the admin dashboard matches the database.
  This requires dummy date and a prebuilt database.
  """
  def test_cart_totals(self):
    self.login('chriscauley',password='dummy_password')
    for resolution in [1,2,7,30]:
      for time_period in [90,180,365,730]:
        data = get_data(time_period=time_period)
        order_items = OrderItem.objects.filter(product__polymorphic_ctype_id=data['product_types'])
        order_items = order_items.filter(order__status__gte=Order.PAID)
        results = self.client.get("/dashboard/totals.json?",data).json()
        for i,day_string in enumerate(results['x']):
          if i%5: #we're just going to skip 4/5 days to make this not take < 10s.
            continue
          start_date = datetime.datetime.strptime(day_string,'%Y-%m-%d').date()
          end_date = start_date + datetime.timedelta(data['resolution'])
          _items = order_items.filter(
            order__created__gte=start_date,
            order__created__lt=end_date,
          )
          amount = sum(_items.values_list('line_total',flat=True))
          self.assertEqual(amount,decimal.Decimal(results['y'][i]))
