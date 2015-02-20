# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RoomGroup'
        db.create_table(u'geo_roomgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'geo', ['RoomGroup'])

        # Deleting field 'Room.geometry'
        db.delete_column(u'geo_room', 'geometry')

        # Deleting field 'Room.color'
        db.delete_column(u'geo_room', 'color')

        # Adding field 'Room.roomgroup'
        db.add_column(u'geo_room', 'roomgroup',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.RoomGroup'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Location.src'
        db.delete_column(u'geo_location', 'src')


    def backwards(self, orm):
        # Deleting model 'RoomGroup'
        db.delete_table(u'geo_roomgroup')

        # Adding field 'Room.geometry'
        db.add_column(u'geo_room', 'geometry',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Room.color'
        db.add_column(u'geo_room', 'color',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Room.roomgroup'
        db.delete_column(u'geo_room', 'roomgroup_id')

        # Adding field 'Location.src'
        db.add_column(u'geo_location', 'src',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    models = {
        u'geo.city': {
            'Meta': {'ordering': "('name',)", 'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latlon': ('geo.widgets.LocationField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'})
        },
        u'geo.dxfentity': {
            'Meta': {'ordering': "('pk',)", 'object_name': 'DXFEntity'},
            'dxftype': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.TextField', [], {}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.Room']", 'null': 'True', 'blank': 'True'})
        },
        u'geo.location': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['geo.City']"}),
            'dxf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latlon': ('geo.widgets.LocationField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.Location']", 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'default': '77007'})
        },
        u'geo.room': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'location'),)", 'object_name': 'Room'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_calendar': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'roomgroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.RoomGroup']", 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'geo.roomgroup': {
            'Meta': {'object_name': 'RoomGroup'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['geo']