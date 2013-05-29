from django.core.mail import mail_admins, send_mail
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from django.conf import settings

from codrspace.models import Photo
from membership.utils import user_from_email

import email, imaplib, os, datetime, time, re

def create_dir(parent,name):
  if not name in os.listdir(parent):
    os.mkdir(os.path.join(parent,name))
  return os.path.join(parent,name)

class Command(BaseCommand):
  def handle(self, *args, **options):
    success = 0
    errors = []
    user_photos = {}
    base_dir = create_dir(settings.MEDIA_ROOT,'attachments')     
    imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
    typ, accountDetails = imapSession.login(settings.PICS_EMAIL,settings.PICS_PASSWORD)
    date_string = datetime.date.today().strftime('%Y-%m-%d')
    if typ != 'OK':
      mail_admins("unable to authenticate email photos",":(")
      raise

    imapSession.select('[Gmail]/All Mail')
    typ, data = imapSession.search(None, 'ALL')
    if typ != 'OK':
      mail_admins('Error searching Inbox.','download_photos failed at searching mailbox')
      raise

    # Iterating over all emails
    for msgId in data[0].split():
      typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
      if typ != 'OK':
        errors.append('Error fetching mail.')
        continue

      mail = email.message_from_string(messageParts[0][1])
      user = None
      try:
        address = re.findall(r'[^><\ @]+@[^><\ @]+',mail['From'])[0]
      except IndexError:
        errors.append("error parsing to_address of:\n\n%s\n\n"%messageParts[0][1])
        continue
      if address:
        user = user_from_email(address)
      for part in mail.walk():
        if part.get_content_maintype() == 'multipart':
          # print part.as_string()
          continue
        if part.get('Content-Disposition') is None:
          # print part.as_string()
          continue
        fname = part.get_filename()
   
        if not bool(fname):
          continue
        fname = "%s-%s"%(int(time.mktime(datetime.datetime.now().utctimetuple())),fname)
        filePath = os.path.join(settings.MEDIA_ROOT, 'attachments', fname)
        fp = open(filePath, 'wb')
        fp.write(part.get_payload(decode=True))
        fp.close()
        photo = Photo(
          filename = fname,
          user = user,
          source = 'email',
          caption = mail['Subject'],
          )
        photo.save()
        success += 1
        if not address in user_photos:
          user_photos[address] = 0

    imapSession.close()
    imapSession.logout()

    if success:
      mail_admins("%s email photos uploaded successfully"%success,"")
    if errors:
      mail_admins("%s errors occurred in getting photos"%len(errors),
                  "The following errors occurred"+"\n\n---------\n".join(errors))

    msg = '%s photos have been uploaded to TX/RX Labs from this email address.'\
        '\n\nTo modify the name and caption on these photos, visit the following url.\n\n%s'
    for addr,count in user_photos.items():
      if not user_from_email(user):
        pass #!
      print addr
      send_mail(
        'New Photos at TX/RX Labs',
        msg%(count,reverse('modify_photos')),
        'noreply@txrxlabs.org',
        [addr]
        )
