# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BulkEmail'
        db.create_table(u'misc_bulkemail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.TextField')()),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'misc', ['BulkEmail'])

        # Adding model 'BulkEmailRecipient'
        db.create_table(u'misc_bulkemailrecipient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('file1', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('file2', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('sent', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'misc', ['BulkEmailRecipient'])


    def backwards(self, orm):
        # Deleting model 'BulkEmail'
        db.delete_table(u'misc_bulkemail')

        # Deleting model 'BulkEmailRecipient'
        db.delete_table(u'misc_bulkemailrecipient')


    models = {
        u'misc.bulkemail': {
            'Meta': {'object_name': 'BulkEmail'},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.TextField', [], {})
        },
        u'misc.bulkemailrecipient': {
            'Meta': {'object_name': 'BulkEmailRecipient'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'file1': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'file2': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['misc']