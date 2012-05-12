from django.test import TestCase
from .models import Task
import datetime

class SimpleTest(TestCase):
  def test_update_occurrence(self):
    """
    Primarily checks to make sure that the update_occurrence method functions properly.
    """
    def _t(task):
      for i,n in enumerate(t.taskoccurrence_set.all()):
        self.assertEqual(n.datetime,now+datetime.timedelta(t.repeat*i))
      
    now = datetime.datetime.now()
    single = Task(name="test",description="test task",repeat=0,first_date=now)
    single.save()
    self.assertEqual(single.taskoccurrence_set.count(),1)
    daily = Task(name="test2",description="test task",repeat=1,first_date=now)
    daily.save()
    self.assertEqual(daily.taskoccurrence_set.all()[0].datetime,now)
    weekly = Task(name="test2",description="test task",repeat=7,first_date=now)
    weekly.save()
