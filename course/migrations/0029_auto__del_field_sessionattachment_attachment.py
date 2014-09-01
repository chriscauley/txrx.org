# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SessionAttachment.attachment'
        db.delete_column(u'course_sessionattachment', 'attachment_id')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'SessionAttachment.attachment'
        raise RuntimeError("Cannot reverse this migration. 'SessionAttachment.attachment' and its values cannot be restored.")

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
        u'auth.user': {
            'Meta': {'ordering': "['username']", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
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
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'course.branding': {
            'Meta': {'object_name': 'Branding'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'small_image_override': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'course.classtime': {
            'Meta': {'ordering': "('start',)", 'object_name': 'ClassTime'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Session']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'course.course': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Course'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'src': (u'sorl.thumbnail.fields.ImageField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['course.Subject']", 'symmetrical': 'False'})
        },
        u'course.coursecompletion': {
            'Meta': {'object_name': 'CourseCompletion'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Course']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'course.coursesubscription': {
            'Meta': {'object_name': 'CourseSubscription'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'course.enrollment': {
            'Meta': {'ordering': "('-datetime',)", 'object_name': 'Enrollment'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'evaluated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'evaluation_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Session']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'course.evaluation': {
            'Meta': {'ordering': "('-datetime',)", 'object_name': 'Evaluation'},
            'content': ('django.db.models.fields.IntegerField', [], {}),
            'content_comments': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enrollment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Enrollment']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'presentation': ('django.db.models.fields.IntegerField', [], {}),
            'presentation_comments': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'question1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'question2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'question3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'question4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'visuals': ('django.db.models.fields.IntegerField', [], {}),
            'visuals_comments': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'course.section': {
            'Meta': {'ordering': "('term', 'course')", 'object_name': 'Section'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Course']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fee': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fee_notes': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['geo.Location']"}),
            'max_students': ('django.db.models.fields.IntegerField', [], {'default': '40'}),
            'no_conflict': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prerequisites': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'requirements': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'safety': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'src': (u'sorl.thumbnail.fields.ImageField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Term']"})
        },
        u'course.session': {
            'Meta': {'ordering': "('section',)", 'object_name': 'Session'},
            'branding': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Branding']", 'null': 'True', 'blank': 'True'}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_dt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Section']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time_string': ('django.db.models.fields.CharField', [], {'default': "'not implemented'", 'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'course.sessionattachment': {
            'Meta': {'ordering': "('order',)", 'object_name': 'SessionAttachment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Session']"})
        },
        u'course.subject': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Subject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'order': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Subject']", 'null': 'True', 'blank': 'True'})
        },
        u'course.term': {
            'Meta': {'ordering': "('-start',)", 'object_name': 'Term'},
            'end': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
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
            'zip_code': ('django.db.models.fields.IntegerField', [], {'default': '77007'})
        }
    }

    complete_apps = ['course']