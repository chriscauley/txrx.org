from rest_framework import serializers

from api.serializers import BaseSizzler
from .models import Event,EventOccurrence

# This I started but then decided to hold off on finishing it
class MonthSizzler(BaseSizzler):
  page_size = 5000 # essentially infinite
  permissions = classmethod(lambda class_, request: request.method == "GET")
  def get_queryset(self):
    # filter a months worth
    # don't show "hidden"
    pass
  class Meta:
    model = EventOccurrence
    fields = ()

class EventOccurrenceSerializer(serializers.ModelSerializer):
  #permissions = lambda class_, request: request.method == "GET"
  class Meta:
    model = EventOccurrence
    fields = ['id','name','total_rsvp','start','end']

# this can't get through jwt so it's dead for now
class EventDetailSizzler(BaseSizzler):
  permissions = classmethod(lambda class_, request: request.method == "GET")
  upcoming_occurrences = EventOccurrenceSerializer(many=True, read_only=True)
  class Meta:
    model = Event
    fields = ['name','room','description','repeat','hidden','allow_rsvp','upcoming_occurrences']
