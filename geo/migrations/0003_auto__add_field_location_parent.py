# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Location.parent'
        db.add_column(u'geo_location', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Location'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Location.parent'
        db.delete_column(u'geo_location', 'parent_id')


    models = {
        u'geo.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latlon': ('geo.widgets.LocationField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'})
        },
        u'geo.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['geo.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latlon': ('geo.widgets.LocationField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.Location']", 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'default': '77007'})
        }
    }

    complete_apps = ['geo']