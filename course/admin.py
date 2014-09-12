from django.contrib import admin
from django import forms
from course.models import Subject, Course, Section, Session, Enrollment, Term, ClassTime, Branding, Evaluation, CourseCompletion
from db.forms import StaffMemberForm

from media.admin import TaggedPhotoInline, TaggedFileInline
from tool.admin import TaggedToolInline

class SubjectAdmin(admin.ModelAdmin):
  exclude = ('order',)

class CourseCompletionInline(admin.TabularInline):
  model = CourseCompletion
  extra = 0
  raw_id_fields = ('user',)

class CourseAdmin(admin.ModelAdmin):
  list_display = ("name","tool_count","photo_count")
  filter_horizontal = ("subjects",)
  inlines = [CourseCompletionInline, TaggedPhotoInline, TaggedToolInline, TaggedFileInline]
  def tool_count(self,obj):
    return len(obj.get_tools())
  def photo_count(self,obj):
    return len(obj.get_photos())

  # duplicated from models.py because of how the admin handles M2M
  def save_related(self, request, form, formsets, change):
    super(CourseAdmin, self).save_related(request, form, formsets, change)
    subjects = form.instance.subjects.all()
    for subject in subjects:
      if subject.parent and not (subject.parent in subjects):
        form.instance.subjects.add(subject.parent)

class ClassTimeInline(admin.TabularInline):
  extra = 0
  model = ClassTime

class SectionAdmin(admin.ModelAdmin):
  save_as = True
  list_display = ("__unicode__","prerequisites","requirements","max_students")
  list_editable = ("prerequisites","requirements","max_students")
  list_filter = ("course__active","location")
  inlines = [TaggedFileInline]
  def has_change_permission(self,request,obj=None):
    if not obj:
      return request.user.is_superuser
    return request.user.is_superuser or (request.user in obj.list_users)
  def has_delete_permission(self,request,obj=None):
    return request.user.is_superuser

class EnrollmentInline(admin.TabularInline):
  model = Enrollment
  readonly_fields = ('user',)
  extra = 0

class SessionAdmin(admin.ModelAdmin):
  form = StaffMemberForm
  raw_id_fields = ('section','user')
  readonly_fields = ('_first_date','get_location')
  list_search = ('section__course__name','user__username')
  list_filter = ("publish_dt",)
  _first_date = lambda self,obj: getattr(obj,'first_date','Will be set on save')
  _first_date.short_description = 'first classtime'
  exclude = ('time_string','slug','publish_dt')
  inlines = (ClassTimeInline, EnrollmentInline, TaggedPhotoInline)
  search_fields = ("user__username","user__email","section__course__name")
  class Media:
    js = ("js/course_admin.js",)

class EnrollmentAdmin(admin.ModelAdmin):
  list_display = ("id",'user', 'session', )
  list_filter = ("session", "user",)
  search_fields = ("user__username","user__email","user__usermembership__paypal_email")
  raw_id_fields = ("user","session")

admin.site.register(Subject,SubjectAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Section,SectionAdmin)
admin.site.register(Enrollment,EnrollmentAdmin)
admin.site.register(Session,SessionAdmin)
admin.site.register(Term)
admin.site.register(Branding)
admin.site.register(Evaluation)
