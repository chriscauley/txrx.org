# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'City'
        db.create_table('geo_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latlon', self.gf('geo.widgets.LocationField')(max_length=500, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2)),
        ))
        db.send_create_signal('geo', ['City'])

        # Adding model 'Location'
        db.create_table('geo_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latlon', self.gf('geo.widgets.LocationField')(max_length=500, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['geo.City'])),
            ('zip_code', self.gf('django.db.models.fields.IntegerField')(default=77007)),
        ))
        db.send_create_signal('geo', ['Location'])


    def backwards(self, orm):
        
        # Deleting model 'City'
        db.delete_table('geo_city')

        # Deleting model 'Location'
        db.delete_table('geo_location')


    models = {
        'geo.city': {
            'Meta': {'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latlon': ('geo.widgets.LocationField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'})
        },
        'geo.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['geo.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latlon': ('geo.widgets.LocationField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'default': '77007'})
        }
    }

    complete_apps = ['geo']
