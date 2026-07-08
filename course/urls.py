from django.urls import path, re_path
from .views import instructor, evaluation, debug_parsing, classes, ajax

urlpatterns = [
  re_path(r'^email/instructor/(\d+)/$',instructor.email,name='email_instructor'),
  re_path(r'^instructor_session/(\d+)/$',instructor.session,name='instructor_session'),

  path('evaluations/',evaluation.index,name='evaluation_index'),
  re_path(r'^evaluation/(\d+)/$',evaluation.detail,name='evaluation_detail'),
  re_path(r'^refuse_evaluation/(\d+)/$',evaluation.refuse,name='evaluation_refuse'),
  path('debug/<int:id>/', debug_parsing,name='debug_parsing'),

  path('', classes.index),
  re_path(r'^(instructor|myclasses)/$',classes.user_ajax,name='user_ajax'),
  re_path(r'^course_(\d+).json$',ajax.course_json),
  path('past_sessions.json', ajax.past_sessions_json),
  path('needed.json',ajax.needed_json),

  re_path(r'^clone_session/(\d+)/$',classes.clone_session,name='clone_session'),
  re_path(r'^u?n?rsvp/(\d+)/',classes.rsvp),
  re_path(r'^term/(\d+)/', classes.index),
  re_path(r'^ics/(all_classes).ics$',classes.ics_classes_all,name='ics_classes_all'),
  re_path(r'^ics/(\d+)/([^/]+)/(my-classes).ics$',classes.ics_classes_user,
      name='ics_classes_user'),
  path('totals/',classes.course_totals,name='course_totals'),
  path('full/',classes.course_full,name='course_full'),
  path('start_checkout/',classes.start_checkout,name='start_checkout'),
  re_path(r'^delay_reschedule/(\d+)/(\d|close)/$', classes.delay_reschedule,
      name='delay_reschedule'),
  re_path(r'^([\w\d\-\_]+)/$',classes.detail_redirect,name='detail_redirect'),
  re_path(r'^(\d+)/([\w\d\-\_]+)/$',classes.detail,name='detail'),
]
