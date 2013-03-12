from django.db import models
from db.models import SlugModel
from tool.models import Tool
#from course.models import Course

class Project(SlugModel):
    parent = models.ForeignKey("self")
    created_on = models.DateTimeField(auto_now_add=True)

class ProjectItem(models.Model):
    name = models.CharField(max_length=64)
    project = models.ForeignKey(Project)
