# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('codrspace_post', 'blog_post')
        db.rename_table('codrspace_banner', 'blog_banner')
        db.rename_table('codrspace_pressitem', 'blog_pressitem')
        db.rename_table('codrspace_setting', 'blog_setting')
        db.rename_table('codrspace_profile', 'blog_profile')
        if not db.dry_run:
            # For permissions to work properly after migrating
            orm['contenttypes.contenttype'].objects.filter(app_label='codrspace', model='post').update(app_label='blog')
            orm['contenttypes.contenttype'].objects.filter(app_label='codrspace', model='banner').update(app_label='blog')
            orm['contenttypes.contenttype'].objects.filter(app_label='codrspace', model='pressitem').update(app_label='blog')
            orm['contenttypes.contenttype'].objects.filter(app_label='codrspace', model='setting').update(app_label='blog')
            orm['contenttypes.contenttype'].objects.filter(app_label='codrspace', model='profile').update(app_label='blog')

    def backwards(self, orm):
        db.rename_table('blog_post', 'codrspace_post')
        db.rename_table('blog_banner', 'codrspace_banner')
        db.rename_table('blog_pressitem', 'codrspace_pressitem')
        db.rename_table('blog_setting', 'codrspace_setting')
        db.rename_table('blog_profile', 'codrspace_profile')
        if not db.dry_run:
            # For permissions to work properly after migrating
            orm['contenttypes.contenttype'].objects.filter(app_label='blog', model='post').update(app_label='codrspace')
            orm['contenttypes.contenttype'].objects.filter(app_label='blog', model='banner').update(app_label='codrspace')
            orm['contenttypes.contenttype'].objects.filter(app_label='blog', model='pressitem').update(app_label='codrspace')
            orm['contenttypes.contenttype'].objects.filter(app_label='blog', model='setting').update(app_label='codrspace')
            orm['contenttypes.contenttype'].objects.filter(app_label='blog', model='profile').update(app_label='codrspace')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },        
    }

    complete_apps = ['codrspace']
