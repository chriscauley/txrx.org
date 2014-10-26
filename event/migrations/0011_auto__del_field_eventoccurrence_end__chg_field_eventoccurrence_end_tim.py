# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'EventOccurrence.end'
        db.delete_column(u'event_eventoccurrence', 'end')


        # Changing field 'EventOccurrence.end_time'
        db.alter_column(u'event_eventoccurrence', 'end_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(0, 0)))
        # Adding field 'Event.room'
        db.add_column(u'event_event', 'room',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Room'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'EventOccurrence.end'
        db.add_column(u'event_eventoccurrence', 'end',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'EventOccurrence.end_time'
        db.alter_column(u'event_eventoccurrence', 'end_time', self.gf('django.db.models.fields.TimeField')(null=True))
        # Deleting field 'Event.room'
        db.delete_column(u'event_event', 'room_id')


    models = {
        u'event.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('wmd.models.MarkDownField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'no_conflict': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'repeat': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.Room']", 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'event.eventoccurrence': {
            'Meta': {'ordering': "('start',)", 'object_name': 'EventOccurrence'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description_override': ('wmd.models.MarkDownField', [], {'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_override': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'publish_dt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'geo.city': {
            'Meta': {'ordering': "('name',)", 'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latlon': ('geo.widgets.LocationField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'})
        },
        u'geo.location': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['geo.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latlon': ('geo.widgets.LocationField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.Location']", 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'default': '77007'})
        },
        u'geo.room': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Room'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['event']