# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ContactSubject'
        db.delete_table(u'contact_contactsubject')

        # Deleting model 'ContactMessage'
        db.delete_table(u'contact_contactmessage')

        # Deleting model 'ContactPerson'
        db.delete_table(u'contact_contactperson')

        # Adding model 'Message'
        db.create_table(u'contact_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.Subject'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.User'], null=True, blank=True)),
        ))
        db.send_create_signal(u'contact', ['Message'])

        # Adding model 'FAQ'
        db.create_table(u'contact_faq', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('answer', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'contact', ['FAQ'])

        # Adding model 'Subject'
        db.create_table(u'contact_subject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.Person'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=9999)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'contact', ['Subject'])

        # Adding model 'SubjectFAQ'
        db.create_table(u'contact_subjectfaq', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.Subject'])),
            ('faq', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.FAQ'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'contact', ['SubjectFAQ'])

        # Adding model 'Person'
        db.create_table(u'contact_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.User'], null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal(u'contact', ['Person'])


    def backwards(self, orm):
        # Adding model 'ContactSubject'
        db.create_table(u'contact_contactsubject', (
            ('contactperson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.ContactPerson'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=9999)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'contact', ['ContactSubject'])

        # Adding model 'ContactMessage'
        db.create_table(u'contact_contactmessage', (
            ('contactsubject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.ContactSubject'])),
            ('from_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.User'], null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'contact', ['ContactMessage'])

        # Adding model 'ContactPerson'
        db.create_table(u'contact_contactperson', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.User'], null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'contact', ['ContactPerson'])

        # Deleting model 'Message'
        db.delete_table(u'contact_message')

        # Deleting model 'FAQ'
        db.delete_table(u'contact_faq')

        # Deleting model 'Subject'
        db.delete_table(u'contact_subject')

        # Deleting model 'SubjectFAQ'
        db.delete_table(u'contact_subjectfaq')

        # Deleting model 'Person'
        db.delete_table(u'contact_person')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contact.faq': {
            'Meta': {'object_name': 'FAQ'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'contact.message': {
            'Meta': {'object_name': 'Message'},
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'from_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contact.Subject']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.User']", 'null': 'True', 'blank': 'True'})
        },
        u'contact.person': {
            'Meta': {'object_name': 'Person'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.User']", 'null': 'True', 'blank': 'True'})
        },
        u'contact.subject': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Subject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '9999'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contact.Person']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'contact.subjectfaq': {
            'Meta': {'ordering': "('order',)", 'object_name': 'SubjectFAQ'},
            'faq': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contact.FAQ']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contact.Subject']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'user.user': {
            'Meta': {'ordering': "('username',)", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['contact']