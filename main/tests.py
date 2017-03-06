from django.test import TestCase, Client
from django.core.management import call_command
from django.core import mail

from lablackey.tests import check_subjects
from event.models import Event, EventOccurrence

import datetime, decimal, six

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

import itertools

def get_data(**kwargs):
    data = {
      'metric': 'line_total',
      'product_types': 214,
      'time_period': 90,
      'resolution': 1
    }
    data.update(**kwargs)
    return data

def get_order_total(start,data,metric=None):
  if isinstance(start,six.string_types):
    start = datetime.datetime.strptime(start,'%Y-%m-%d').date()
  end = start + datetime.timedelta(data['resolution'])
  order_items = OrderItem.objects.filter(product__polymorphic_ctype_id=data['product_types'])
  order_items = order_items.filter(order__status__gte=Order.PAID)
  _items = order_items.filter(
    order__created__gte=start,
    order__created__lt=end,
  )
  return sum(_items.values_list(metric or data['metric'],flat=True))

def get_all_payments(start,data):
  total = get_order_total(start,data,metric="line_total")
  if isinstance(start,six.string_types):
    start = datetime.datetime.strptime(start,'%Y-%m-%d').date()
  end = start + datetime.timedelta(data['resolution'])
  total += sum(Status.objects.filter(datetime__gte=start,datetime__lt=end).values_list("amount",flat=True))
  return total

resolutions_time_periods = itertools.product([1,2,7,30],[90,180,365,730])

class DashboardTest(ClientTestCase):
  """
  Test that the data coming out of the admin dashboard matches the database.
  This requires dummy date and a prebuilt database.
  """
  def setUp(self):
    self.login('chriscauley',password='dummy_password')
  def get_json(self,data):
    return self.client.get("/dashboard/totals.json?",data).json()
  def test_order_totals(self):
    for metric in ['quantity','line_total']:
      for resolution, time_period in resolutions_time_periods:
        data = get_data(time_period=time_period,metric=metric)
        results = self.get_json(data)
        for i,day_string in enumerate(results['x']):
          if i%5: #we're just going to skip 4/5 days to make this not take < 10s.
            continue
          print get_order_total(day_string,data), decimal.Decimal(results['y'][i])
          self.assertEqual(
            get_order_total(day_string,data),
            decimal.Decimal(results['y'][i])
          )
  def test_all_payments(self):
    for resolution, time_period in resolutions_time_periods:
      data = get_data(time_period=time_period,resolution=resolution,metric="all_payments")
      results = self.get_json(data)
      for i,day_string in enumerate(results['x']):
        if i%5:
          continue
        self.assertEqual(
          decimal.Decimal(results['y'][i]),
          get_all_payments(day_string,data)
        )
