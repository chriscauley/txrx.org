import os, django; os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings';django.setup()
from django.utils import timezone

from event.models import Event, RepeatEvent

# fix Friday Open House
if Event.objects.filter(id=124): # event to be deleted
  old = Event.objects.get(id=124) # third friday
  new = Event.objects.get(id=1) # first friday
  new_repeat,_new = new.repeatevent_set.get_or_create(
    first_date='2017-3-3',
    start='19:00',
    end='21:00',
    repeat_flavor='start-month',
  )
  new.upcoming_occurrences.update(repeatevent=new_repeat)
  old_repeat,_new = new.repeatevent_set.get_or_create(
    first_date='2017-2-17',
    start='19:00',
    end='21:00',
    repeat_flavor='start-month',
  )
  old.upcoming_occurrences.update(repeatevent=old_repeat)
  old.eventoccurrence_set.all().update(event=new)
  new.repeat = None
  new.save()
  print "deleting: ",old
  old.delete()

orientations = Event.objects.get(id=105)
orientations.repeatevent_set.all().delete()
if not orientations.repeatevent_set.all():
  sunday,_new = orientations.repeatevent_set.get_or_create(
    first_date='2017-02-19',
    start='13:00',
    end='13:30',
    repeat_flavor='weekly'
  )
  tuesday,_new = orientations.repeatevent_set.get_or_create(
    first_date='2017-02-14',
    start='19:00',
    end='19:30',
    repeat_flavor='weekly'
  )
  friday,_new = orientations.repeatevent_set.get_or_create(
    first_date='2017-02-17',
    start='12:00',
    end='12:30',
    repeat_flavor='weekly'
  )
  for occ in orientations.upcoming_occurrences:
    dow = occ.start.isoweekday()
    if dow == 7: # sunday
      occ.repeatevent = sunday
      occ.end_time = '13:30'
    if dow == 2:
      occ.repeatevent = tuesday
      occ.end_time = '19:30'
    if dow == 5:
      occ.repeatevent = friday
      occ.end_time = '12:30'
    occ.save()
  orientations.repeat = None
  orientations.save()

RepeatEvent.objects.all()[0].generate(start_datetime=timezone.now())

tinkertime = Event.objects.get(id=15)
tinkertime.repeatevent_set.all().delete()
if not tinkertime.repeatevent_set.all():
  tinkertime.upcoming_occurrences.delete() # we're just going to respawn these
  friday,_new = orientations.repeatevent_set.get_or_create(
    first_date='2017-02-17',
    start='10:00',
    end='22:00',
    repeat_flavor='weekly'
  )
  saturday,_new = orientations.repeatevent_set.get_or_create(
    first_date='2017-02-18',
    start='9:00',
    end='20:00',
    repeat_flavor='weekly'
  )
  sunday,_new = orientations.repeatevent_set.get_or_create(
    first_date='2017-02-19',
    start='10:00',
    end='19:00',
    repeat_flavor='weekly'
  )
  [RepeatEvent.objects.get(id=d.id).generate(start_datetime=timezone.now()) for d in [friday, saturday, sunday]]
