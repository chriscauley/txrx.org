from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend

class DebugBackend(EmailBackend):
  def send_messages(self,email_messages):
    if True:# not settings.DEBUG:
      return super(DebugBackend,self).send_messages(email_messages)
    for message in email_messages:
      message.to = filter_emails(message.to) or [getattr(settings,'ALLOWED_EMAILS',[])[0]]
      message.cc = filter_emails(message.cc)
      message.bcc = filter_emails(message.bcc)
    return super(DebugBackend,self).send_messages(email_messages)

def filter_emails(emails):
  if settings.DEBUG:
    #only email certain people from dev server!
    return [e for e in emails if e in getattr(settings,'ALLOWED_EMAILS',[])]
  return emails
