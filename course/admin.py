from django.contrib import admin
from django import forms
from course.models import Subject, Course, Section, Session, Enrollment, Term, ClassTime, Branding, Evaluation, SessionAttachment
from db.forms import StaffMemberForm

from codrspace.admin import PhotoSetConnectionInline

class SubjectAdmin(admin.ModelAdmin):
  pass

class SectionInline(admin.TabularInline):
  extra = 0
  model = Section

class CourseAdmin(admin.ModelAdmin):
  list_display = ("name",)
  filter_horizontal = ("subjects",)
  #inlines = (SectionInline,)

class ClassTimeInline(admin.TabularInline):
  extra = 0
  model = ClassTime

class SectionAdmin(admin.ModelAdmin):
  save_as = True
  list_display = ("__unicode__","prerequisites","requirements","max_students")
  list_editable = ("prerequisites","requirements","max_students")
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

class SessionAttachmentInline(admin.TabularInline):
  model = SessionAttachment
  extra = 0

class SessionAdmin(admin.ModelAdmin):
  form = StaffMemberForm
  raw_id_fields = ('section',)
  exclude = ('time_string','slug')
  extra = 0
  inlines = (PhotoSetConnectionInline, ClassTimeInline, EnrollmentInline,SessionAttachmentInline)

class EnrollmentAdmin(admin.ModelAdmin):
  list_display = ("id",'user', 'session', )
  list_filter = ("session", "user",)
  search_fields = ("user__username","user__email","user__usermembership__paypal_email")

admin.site.register(Subject,SubjectAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Section,SectionAdmin)
admin.site.register(Enrollment,EnrollmentAdmin)
admin.site.register(Session,SessionAdmin)
admin.site.register(Term)
admin.site.register(Branding)
admin.site.register(Evaluation)
