from django.db import models
from lablackey.profile.models import UserModel
from db.models import SlugModel
from tool.models import Tool
#from course.models import Course

class Project(SlugModel,UserModel):
    parent = models.ForeignKey("self")
    created_on = models.DateTimeField(auto_now_add=True)

class ProjectItem(UserModel):
    name = models.CharField(max_length=64)
    project = models.ForeignKey(Project)
