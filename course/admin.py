from django.contrib import admin
from django import forms
from db.forms import StaffMemberForm
from db.admin import NamedTreeModelAdmin

from .models import Subject, Course, Session, Enrollment, Term, ClassTime, Branding, Evaluation, CourseCompletion
from event.admin import OccurrenceModelInline
from media.admin import TaggedPhotoInline, TaggedFileInline
from tool.admin import TaggedToolInline

class CourseCompletionInline(admin.TabularInline):
  model = CourseCompletion
  extra = 0
  raw_id_fields = ('user',)

class CourseAdmin(admin.ModelAdmin):
  list_display = ("name","tool_count","photo_count")
  readonly_fields = ("_notifies",)
  filter_horizontal = ("subjects",)
  inlines = [CourseCompletionInline, TaggedPhotoInline, TaggedToolInline, TaggedFileInline]
  def tool_count(self,obj):
    return len(obj.get_tools())
  def photo_count(self,obj):
    return len(obj.get_photos())
  def _notifies(self,obj):
    out = ''
    for notify in obj.notifycourse_set.all():
      out += "%s<br/>"%notify.user.email
    return out
  _notifies.allow_tags = True
  # duplicated from models.py because of how the admin handles M2M
  def save_related(self, request, form, formsets, change):
    super(CourseAdmin, self).save_related(request, form, formsets, change)
    subjects = form.instance.subjects.all()
    for subject in subjects:
      if subject.parent and not (subject.parent in subjects):
        form.instance.subjects.add(subject.parent)

class ClassTimeInline(OccurrenceModelInline):
  extra = 0
  model = ClassTime

class EnrollmentInline(admin.TabularInline):
  model = Enrollment
  readonly_fields = ('user',)
  extra = 0

class SessionAdmin(admin.ModelAdmin):
  form = StaffMemberForm
  ordering = ('-first_date',)
  raw_id_fields = ('course','user')
  readonly_fields = ('_first_date','get_room')
  #list_search = ('course__course__name','user__username')
  list_filter = ("publish_dt",)
  _first_date = lambda self,obj: getattr(obj,'first_date','Will be set on save')
  _first_date.short_description = 'first classtime'
  exclude = ('time_string','slug','publish_dt')
  inlines = (ClassTimeInline, EnrollmentInline, TaggedPhotoInline)
  search_fields = ("user__username","user__email","course__name")
  class Media:
    js = ("js/course_admin.js",)

class EnrollmentAdmin(admin.ModelAdmin):
  list_display = ("id",'user', 'session', )
  list_filter = ("session", "user",)
  search_fields = ("user__username","user__email","user__usermembership__paypal_email")
  raw_id_fields = ("user","session")

class EvaluationAdmin(admin.ModelAdmin):
  raw_id_fields = ('user','enrollment')

admin.site.register(Subject,NamedTreeModelAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Enrollment,EnrollmentAdmin)
admin.site.register(Session,SessionAdmin)
admin.site.register(Term)
admin.site.register(Branding)
admin.site.register(Evaluation,EvaluationAdmin)
