from django.conf import settings
from django.contrib import admin
from django import forms
from lablackey.db.forms import StaffMemberForm
from lablackey.db.admin import NamedTreeModelAdmin, RawMixin

from .models import Subject, Course, CourseRoomTime, Session, Enrollment, Term, ClassTime, Branding, Evaluation, CourseEnrollment, SessionProduct
from event.admin import OccurrenceModelInline
from lablackey.contenttypes import get_contenttype
from media.admin import TaggedFileInline, TaggedPhotoAdmin
from notify.models import Follow
from tool.admin import TaggedToolInline

class CourseRoomTimeInline(admin.TabularInline):
  model = CourseRoomTime
  extra = 0

@admin.register(Course)
class CourseAdmin(TaggedPhotoAdmin):
  list_display = ("name","_follow_count","active","tool_count","photo_count","content","visuals","presentation")
  list_editable = ("content","visuals","presentation")
  readonly_fields = ("_follow",)
  filter_horizontal = ("subjects",)
  search_fields = ("name",)
  inlines = [CourseRoomTimeInline, TaggedToolInline, TaggedFileInline]
  def tool_count(self,obj):
    return len(obj.get_tools())
  def photo_count(self,obj):
    return len(obj.get_photos())
  def _follow_count(self,obj):
    return Follow.objects.filter(content_type=get_contenttype(obj),object_id=obj.id).count()
  def _follow(self,obj):
    _click = "href='javascript:;' onclick='$(this).siblings().toggle();'"
    out = "<a %s><b>%s follow (click to toggle)</b></a>"%(_click,self._follow_count(obj))
    for notify in Follow.objects.filter(content_type=get_contenttype(obj),object_id=obj.id):
      out += "<div style='display: none;'>%s</div>"%notify.user.email
    return out
  _follow.allow_tags = True
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
  readonly_fields = ("emailed",)

class CourseEnrollmentInline(admin.TabularInline):
  model = CourseEnrollment
  readonly_fields = ("user","course","datetime","quantity")
  extra = 0

class EnrollmentInline(admin.TabularInline):
  model = Enrollment
  readonly_fields = ('user','session')
  exclude = ('completed','evaluated','emailed','transaction_ids','evaluation_date')
  extra = 0

class SessionProductInline(admin.TabularInline):
  model = SessionProduct
  extra = 0

@admin.register(Session)
class SessionAdmin(TaggedPhotoAdmin):
  form = StaffMemberForm
  ordering = ('-first_date',)
  raw_id_fields = ('course','user')
  readonly_fields = ('_first_date','_last_date','get_room')
  list_display = ("__unicode__","first_date","active")
  list_filter = ("publish_dt",'active')
  _first_date = lambda self,obj: getattr(obj,'first_date','Will be set on save')
  _first_date.short_description = 'first classtime'
  _last_date = lambda self,obj: getattr(obj,'last_date','Will be set on save')
  _last_date.short_description = 'last classtime'
  exclude = ('time_string','slug','publish_dt')
  inlines = [ClassTimeInline, EnrollmentInline]
  if settings.DEBUG: # I like to see this sometimes for debug purchases
    inlines.append(SessionProductInline)
  search_fields = ("user__username","user__email","course__name")
  class Media:
    js = ("js/course_admin.js",)

@admin.register(Enrollment)
class EnrollmentAdmin(RawMixin,admin.ModelAdmin):
  list_display = ("id",'user', 'session','datetime')
  search_fields = ("user__username","user__email","user__paypal_email","user__first_name","user__last_name")
  raw_id_fields = ("user","session")

@admin.register(Evaluation)
class EvaluationAdmin(RawMixin,admin.ModelAdmin):
  exclude = ('user','enrollment','anonymous')
  readonly_fields = ('get_user',)

admin.site.register(Subject,NamedTreeModelAdmin)
admin.site.register(Term)
admin.site.register(Branding)
