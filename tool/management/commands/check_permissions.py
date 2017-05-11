from django.conf import settings
from django.core.management.base import BaseCommand

from course.models import Session
from membership.models import Flag, add_months
from tool.models import UserCriterion

import datetime

class Command(BaseCommand):
  def handle(self,*args,**kwargs):
    now = datetime.datetime.now()
    safety_criteria = UserCriterion.active_objects.filter(criterion_id=settings.SAFETY_CRITERION_ID)
    permanent_criteria = safety_criteria.exclude(content_type__model="subscription")

    # Find any remaining safety flags that need cleaning up
    safety_flags = Flag.objects.filter(status__in=['new_safety','safety_emailed','safety_expired'])
    for flag in safety_flags:
      if permanent_criteria.filter(user=flag.subscription.user):
        # this user took the safety class, nuke the flag
        flag.apply_status("safety_completed",mail=False)

    # email anyone who must go to the next safety criteria or lose the permission
    temporary_criteria = safety_criteria.filter(content_type__model="subscription")
    safety_sessions = Session.objects.filter(course_id=settings.SAFETY_ID)
    try:
      next_safety = safety_sessions.filter(
        first_date__gte=now+datetime.timedelta(7),
        first_date__lte=now+datetime.timedelta(8),
      )[0]
    except IndexError:
      pass
    else:
      # there's a safety class in exactly a week, send out reminders
      # if they signed up before this date they must take this safety class
      needs_mail = []
      sign_up_date = add_months(next_safety.first_date,-2)
      if options.get("verbosity") > 0:
        print sign_up_date
      for criterion in temporary_criteria.filter(created__lte=sign_up_date):
        if options.get("verbosity") > 0:
          print 'next',next_safety
        defaults = {'status': 'new_safety'}
        flag, new = Flag.objects.get_or_create(
          subscription=criterion.content_object,
          reason="safety",
          defaults=defaults,
        )
        if flag.subscription.user.enrollment_set.filter(session=next_safety):
          #they are signed up, so don't email them
          continue
        if flag.status == "safety_expired":
          # flag.apply_status("emailed_safety")
          needs_mail.append("http://txrxlabs.org/admin/membership/flag/%s/"%flag.pk)
      if needs_mail:
        mail_admins("Remind these people about safety","\n".join(needs_mail))

    # Remove permissions for these guys
    try:
      last_safety = safety_sessions.filter(
        first_date__gte=now-datetime.timedelta(1),
        first_date__lte=now,
      )[0]
    except IndexError:
      pass
    else:
      # there was a safety yesterday. Delete any relevant temporary criteria.
      sign_up_date = add_months(last_safety.first_date,-2)
      for criterion in temporary_criteria.filter(created__lte=sign_up_date):
        try:
          flag = safety_flags.get(subscription__user=criterion.user)
          flag.apply_status('safety_expired',mail=False)
        except Flag.DoesNotExist:
          pass
        criterion.delete()
