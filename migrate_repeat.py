import os, django; os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings';django.setup()
from django.utils import timezone

from event.models import Event, EventRepeat

# fix Friday Open House
if Event.objects.filter(id=124): # event to be deleted
  old = Event.objects.get(id=124) # third friday
  new = Event.objects.get(id=1) # first friday
  new_repeat,_new = new.eventrepeat_set.get_or_create(
    first_date='2017-3-3',
    start_time='19:00',
    end_time='21:00',
    repeat_flavor='start-month',
  )
  new.upcoming_occurrences.update(eventrepeat=new_repeat)
  old_repeat,_new = new.eventrepeat_set.get_or_create(
    first_date='2017-2-17',
    start_time='19:00',
    end_time='21:00',
    repeat_flavor='start-month',
  )
  old.upcoming_occurrences.update(eventrepeat=old_repeat)
  old.eventoccurrence_set.all().update(event=new)
  print "deleting: ",old
  old.delete()

orientations = Event.objects.get(id=105)
if not orientations.eventrepeat_set.all():
  sunday,_new = orientations.eventrepeat_set.get_or_create(
    first_date='2017-02-19',
    start_time='13:00',
    end_time='13:30',
    repeat_flavor='weekly'
  )
  tuesday,_new = orientations.eventrepeat_set.get_or_create(
    first_date='2017-02-14',
    start_time='19:00',
    end_time='19:30',
    repeat_flavor='weekly'
  )
  friday,_new = orientations.eventrepeat_set.get_or_create(
    first_date='2017-02-17',
    start_time='12:00',
    end_time='12:30',
    repeat_flavor='weekly'
  )
  for occ in orientations.upcoming_occurrences:
    dow = occ.start.isoweekday()
    if dow == 7: # sunday
      occ.eventrepeat = sunday
      occ.end_time = '13:30'
    if dow == 2:
      occ.eventrepeat = tuesday
      occ.end_time = '19:30'
    if dow == 5:
      occ.eventrepeat = friday
      occ.end_time = '12:30'
    occ.save()
  orientations.repeat = None
  orientations.save()

EventRepeat.objects.all()[0].generate(start_datetime=timezone.now())

tinkertime = Event.objects.get(id=15)
if not tinkertime.eventrepeat_set.all():
  print "in tinker time!"
  friday,_new = tinkertime.eventrepeat_set.get_or_create(
    first_date='2017-02-17',
    start_time='10:00',
    end_time='22:00',
    repeat_flavor='weekly'
  )
  saturday,_new = tinkertime.eventrepeat_set.get_or_create(
    first_date='2017-02-18',
    start_time='9:00',
    end_time='20:00',
    repeat_flavor='weekly'
  )
  sunday,_new = tinkertime.eventrepeat_set.get_or_create(
    first_date='2017-02-19',
    start_time='10:00',
    end_time='19:00',
    repeat_flavor='weekly'
  )
  [EventRepeat.objects.get(id=d.id).generate(start_datetime=timezone.now()) for d in [friday, saturday, sunday]]

for event in Event.objects.filter(repeat__isnull=False):
  if event.repeat == 'month-dow':
    flavor = 'start-month'
  elif event.repeat == 'weekly':
    flavor = 'weekly'
  else:
    print "not repeating %s"%event.repeat
    continue
  eventrepeat,_new = event.eventrepeat_set.get_or_create(
    first_date=event.upcoming_occurrences[0].start.date(),
    start_time=event.upcoming_occurrences[0].start.time(),
    end_time=event.upcoming_occurrences[0].end_time,
    repeat_flavor=flavor,
  )
  if _new:
    print "Created EventRepeat: %s"%eventrepeat
  event.upcoming_occurrences.update(eventrepeat=eventrepeat)

#for event in Event.objects.filter(repeat='weekly'):
