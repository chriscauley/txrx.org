from django.conf import settings
from django.http import HttpResponse
from django.template.defaultfilters import slugify

import icalendar
from pytz import timezone,utc

def make_ics(occurrences=None,title=None):
  """Generate an ics file from an list of occurrences.
     Each occurrence object must have
       obj.description - TextArea (plain text)
       obj.name - CharField
       obj.start - DateTimeField
       obj.end - DatetimeField (Optional)
       obj.get_absolute_url() - a method that returns a url without a domain
     """
  tz = timezone(settings.TIME_ZONE)

  name = "%s @ %s"%(title,settings.SITE_NAME)
  calObj = icalendar.Calendar()
  calObj.add('method', 'PUBLISH')  # IE/Outlook needs this
  calObj.add('version','2.0')
  calObj.add('prodid', '-//%s calendar product//mxm.dk//'%settings.SITE_NAME)

  calObj.add('x-wr-calname', name)
  calObj.add('name', name)

  for occ in occurrences:
    vevent = icalendar.Event()
    start_dt = tz.localize(occ.start)
    start_dt = start_dt.astimezone(utc)

    vevent['uid'] = '%s%d'%(slugify(settings.SITE_NAME),occ.id)
    vevent.add('dtstamp', start_dt)
    vevent.add('dtstart', start_dt)
    if occ.end:
      end_dt = tz.localize(occ.end)
      end_dt = end_dt.astimezone(utc)
      vevent.add('dtend', end_dt)

    vevent.add('summary', occ.name)
    vevent.add('url', '%s%s'%(settings.SITE_URL, occ.get_absolute_url()))
    vevent.add('class', 'PUBLIC')
    vevent.add('x-microsoft-cdo-importance', '1')
    vevent.add('priority', '5')
    vevent.add('description', occ.description)
    vevent.add('location', str(occ.get_location()))

    calObj.add_component(vevent)

  return calObj

def ics2response(calendar_object,fname):
  icalstream = calendar_object.to_ical().replace('TZID=UTC;', '')

  response = HttpResponse(icalstream, mimetype='text/calendar')

  response['Filename'] = '%s.ics'%fname
  response['Content-Disposition'] = 'attachment; filename=%s.ics'%fname
  response['Content-Length'] = len(icalstream)

  return response
