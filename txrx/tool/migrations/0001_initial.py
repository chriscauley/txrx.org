# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lab'
        db.create_table('tool_lab', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('src', self.gf('sorl.thumbnail.fields.ImageField')(max_length=300, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=9999)),
        ))
        db.send_create_signal('tool', ['Lab'])

        # Adding model 'Tool'
        db.create_table('tool_tool', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tool.Lab'])),
            ('make', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=9999)),
            ('thumbnail', self.gf('sorl.thumbnail.fields.ImageField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal('tool', ['Tool'])

        # Adding model 'ToolVideo'
        db.create_table('tool_toolvideo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tool', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tool.Tool'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=9999)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('embed_code', self.gf('django.db.models.fields.TextField')()),
            ('thumbnail', self.gf('sorl.thumbnail.fields.ImageField')(max_length=300, null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Project'], null=True, blank=True)),
        ))
        db.send_create_signal('tool', ['ToolVideo'])

        # Adding model 'ToolLink'
        db.create_table('tool_toollink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tool', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tool.Tool'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=9999)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('tool', ['ToolLink'])

        # Adding model 'ToolPhoto'
        db.create_table('tool_toolphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=9999)),
            ('tool', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tool.Tool'])),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photo.Photo'])),
            ('caption_override', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal('tool', ['ToolPhoto'])

    def backwards(self, orm):
        # Deleting model 'Lab'
        db.delete_table('tool_lab')

        # Deleting model 'Tool'
        db.delete_table('tool_tool')

        # Deleting model 'ToolVideo'
        db.delete_table('tool_toolvideo')

        # Deleting model 'ToolLink'
        db.delete_table('tool_toollink')

        # Deleting model 'ToolPhoto'
        db.delete_table('tool_toolphoto')

    models = {
        'articles.article': {
            'Meta': {'ordering': "('-publish_date', 'title')", 'object_name': 'Article'},
            'addthis_use_author': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'addthis_username': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'auto_tag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'followup_for': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'followups'", 'blank': 'True', 'to': "orm['articles.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'markup': ('django.db.models.fields.CharField', [], {'default': "'h'", 'max_length': '1'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'related_articles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_articles_rel_+'", 'blank': 'True', 'to': "orm['articles.Article']"}),
            'rendered_content': ('django.db.models.fields.TextField', [], {}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.ArticleStatus']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['articles.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'use_addthis_button': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'articles.articlestatus': {
            'Meta': {'ordering': "('ordering', 'name')", 'object_name': 'ArticleStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_live': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'articles.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
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
        'photo.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'project.project': {
            'Meta': {'ordering': "('-publish_date', 'title')", 'object_name': 'Project', '_ormbases': ['articles.Article']},
            'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['articles.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'tool.lab': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Lab'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '9999'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'src': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'tool.tool': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Tool'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tool.Lab']"}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '9999'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'thumbnail': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'tool.toollink': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ToolLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '9999'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'tool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tool.Tool']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'tool.toolphoto': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ToolPhoto'},
            'caption_override': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '9999'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['photo.Photo']"}),
            'tool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tool.Tool']"})
        },
        'tool.toolvideo': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ToolVideo'},
            'embed_code': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '9999'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Project']", 'null': 'True', 'blank': 'True'}),
            'thumbnail': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'tool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tool.Tool']"})
        }
    }

    complete_apps = ['tool']