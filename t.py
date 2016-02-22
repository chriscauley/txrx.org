import os
os.environ['DJANGO_SETTINGS_MODULE']='main.settings'
from course.models import Course

print len(Course.objects.needs_reschedule())
