from django.utils import unittest
from .models import InstagramPhoto, InstagramLocation, InstagramUser, InstagramTag

class SimpleTest(unittest.TestCase):
    def setUp(self):
      self.tag = InstagramTag(name="txrx")
      self.tag.save()
      self.location= InstagramLocation(iid=65957079)

    def test_models(self):
        """Animals that can speak are correctly identified"""
        self.tag.follow_me()
        self.assertTrue(self.tag.instagramphoto_set.count()>0)
