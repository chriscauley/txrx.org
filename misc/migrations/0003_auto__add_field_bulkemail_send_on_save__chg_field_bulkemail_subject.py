# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BulkEmail.send_on_save'
        db.add_column(u'misc_bulkemail', 'send_on_save',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'BulkEmail.subject'
        db.alter_column(u'misc_bulkemail', 'subject', self.gf('django.db.models.fields.CharField')(max_length=128))

    def backwards(self, orm):
        # Deleting field 'BulkEmail.send_on_save'
        db.delete_column(u'misc_bulkemail', 'send_on_save')


        # Changing field 'BulkEmail.subject'
        db.alter_column(u'misc_bulkemail', 'subject', self.gf('django.db.models.fields.TextField')())

    models = {
        u'misc.bulkemail': {
            'Meta': {'object_name': 'BulkEmail'},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_on_save': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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