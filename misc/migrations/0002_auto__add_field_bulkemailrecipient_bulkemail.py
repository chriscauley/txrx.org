# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BulkEmailRecipient.bulkemail'
        db.add_column(u'misc_bulkemailrecipient', 'bulkemail',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['misc.BulkEmail']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BulkEmailRecipient.bulkemail'
        db.delete_column(u'misc_bulkemailrecipient', 'bulkemail_id')


    models = {
        u'misc.bulkemail': {
            'Meta': {'object_name': 'BulkEmail'},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.TextField', [], {})
        },
        u'misc.bulkemailrecipient': {
            'Meta': {'object_name': 'BulkEmailRecipient'},
            'bulkemail': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['misc.BulkEmail']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'file1': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'file2': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['misc']