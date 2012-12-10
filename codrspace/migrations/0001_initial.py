# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Post'
        db.create_table('codrspace_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=75)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(default=0, max_length=30)),
            ('publish_dt', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('create_dt', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_dt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('codrspace', ['Post'])

        # Adding unique constraint on 'Post', fields ['slug', 'author']
        db.create_unique('codrspace_post', ['slug', 'author_id'])

        # Adding model 'Media'
        db.create_table('codrspace_media', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('upload_dt', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('codrspace', ['Media'])

        # Adding model 'Setting'
        db.create_table('codrspace_setting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blog_title', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('blog_tagline', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timezone', self.gf('timezones.fields.TimeZoneField')(default='US/Central', max_length=100)),
        ))
        db.send_create_signal('codrspace', ['Setting'])

        # Adding model 'Profile'
        db.create_table('codrspace_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('git_access_token', self.gf('django.db.models.fields.CharField')(max_length=75, null=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('meta', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('codrspace', ['Profile'])


    def backwards(self, orm):
        # Removing unique constraint on 'Post', fields ['slug', 'author']
        db.delete_unique('codrspace_post', ['slug', 'author_id'])

        # Deleting model 'Post'
        db.delete_table('codrspace_post')

        # Deleting model 'Media'
        db.delete_table('codrspace_media')

        # Deleting model 'Setting'
        db.delete_table('codrspace_setting')

        # Deleting model 'Profile'
        db.delete_table('codrspace_profile')


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
            'Meta': {'ordering': "['username']", 'object_name': 'User'},
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
        'codrspace.media': {
            'Meta': {'object_name': 'Media'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upload_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'codrspace.post': {
            'Meta': {'unique_together': "(('slug', 'author'),)", 'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'create_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '75'}),
            'status': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '30'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'update_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'codrspace.profile': {
            'Meta': {'object_name': 'Profile'},
            'git_access_token': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'codrspace.setting': {
            'Meta': {'object_name': 'Setting'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'blog_tagline': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'blog_title': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'timezone': ('timezones.fields.TimeZoneField', [], {'default': "'US/Central'", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['codrspace']