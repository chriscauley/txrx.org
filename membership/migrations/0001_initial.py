# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Membership'
        db.create_table('membership_membership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('monthly', self.gf('django.db.models.fields.IntegerField')()),
            ('yearly', self.gf('django.db.models.fields.IntegerField')()),
            ('student_rate', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('membership', ['Membership'])

        # Adding model 'Role'
        db.create_table('membership_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('membership', ['Role'])

        # Adding model 'Feature'
        db.create_table('membership_feature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('membership', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['membership.Membership'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('membership', ['Feature'])

        # Adding model 'Profile'
        db.create_table('membership_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('ghandle', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('membership', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['membership.Membership'])),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('avatar', self.gf('sorl.thumbnail.fields.ImageField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal('membership', ['Profile'])

        # Adding model 'Survey'
        db.create_table('membership_survey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('reasons', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('projects', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('skills', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('expertise', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('questions', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('membership', ['Survey'])

    def backwards(self, orm):
        # Deleting model 'Membership'
        db.delete_table('membership_membership')

        # Deleting model 'Role'
        db.delete_table('membership_role')

        # Deleting model 'Feature'
        db.delete_table('membership_feature')

        # Deleting model 'Profile'
        db.delete_table('membership_profile')

        # Deleting model 'Survey'
        db.delete_table('membership_survey')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'membership.feature': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Feature'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['membership.Membership']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'membership.membership': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Membership'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monthly': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'student_rate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yearly': ('django.db.models.fields.IntegerField', [], {})
        },
        'membership.profile': {
            'Meta': {'object_name': 'Profile'},
            'avatar': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ghandle': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['membership.Membership']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'membership.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'membership.survey': {
            'Meta': {'object_name': 'Survey'},
            'expertise': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projects': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'questions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reasons': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'skills': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['membership']