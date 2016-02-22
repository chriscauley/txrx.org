from django.db import models

from lablackey.db.models import UserModel
from course.models import Session, Course

class NotifyCourse(UserModel):
  course = models.ForeignKey(Course)
  __unicode__ = lambda self: "{} -- {}".format(self.user,self.course)
  class Meta:
    unique_together = ('course','user')
