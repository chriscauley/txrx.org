from django.core.management.base import BaseCommand

from membership.models import UserFlag, EMAIL_REASONS

from lablackey.mail import send_template_email, print_to_mail
import datetime

class Command(BaseCommand):
  @print_to_mail
  def handle(self, *args, **options):
    print [f.datetime for f in flags]
    print EMAIL_REASONS['payment_overdue']
    now = datetime.datetime.now()
    day = datetime.timedelta(1)
    first_warning = 1
    second_warning = 7
    final_warning = 2
    #email anyone whos flag is ten or more days old
    flags = UserFlag.objects.filter(emailed__isnull=True)
    overdue_flags = flags.filter(reason__in=EMAIL_REASONS['payment_overdue'],datetime__lte=now-1*day)
    print list(overdue_flags)
    email_tuples = [
      ('first_warning', first_warning),
      ('second_warning', second_warning),
      ('final_warning', final_warning+second_warning)
    ]
    email_dict = dict(email_tuples)
    for template,num_days in email_tuples:
      for flag in overdue_flags:
        context = {
          'user': flag.user,
          'subscription': flag.content_object
        }
        context.update(email_dict)
        send_template_email('email/overdue/%'%template,flag.user.email,context=context)
        flag.emailed = now
        flag.save()
    if overdue_flags:
      mail_admins("Overdue emails sent","for flags %s"%([f.pk for f in overdue_flags]))
