from django.test import TestCase
from .models import Membership, Group

def setUp():
  objects = [
    (Group,[
      {"name": "Non-Tool", "order": 3, 'pk': 1},
      {"name": "All Access", "order": 0, 'pk':3},
    ]),
    (Membership,[
      {"discount_percentage": 0, "group": 1, "name": "Non-paying Member", "order": 0},
      {"discount_percentage": 10, "group": 3, "name": "Tinkerer", "order": 20},
      {"discount_percentage": 10, "group": 3, "name": "Hacker", "order": 21},
      {"discount_percentage": 10, "group": 3, "name": "Table Hacker", "order": 22},
      {"discount_percentage": 0, "group": 1, "name": "TX/RX Supporter", "order": 1},
      {"discount_percentage": 5, "group": 1, "name": "Amigotron", "order": 2},
    ]),
  ]
  for model,kwargs in objects:
    model.objects.create(**kwargs)

class SimpleTest(TestCase):
  def setUp(self):
    setUp()
  def test_dummy(self):
    self.assertEqual(1 + 1, 2)
