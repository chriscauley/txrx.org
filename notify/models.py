from django.db import models

from db.models import UserModel
from course.models import Session, Course

class NotifyCourse(UserModel):
  course = models.ForeignKey(Course)
  #session = models.ForeignKey(Session)
  __unicode__ = lambda self: "{} -- {}".format(self.user,self.course)
  class Meta:
    unique_together = ('course','user')
