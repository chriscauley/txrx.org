# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'ToolSlide'
        db.delete_table('tool_toolslide')

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

        # Adding model 'ToolPhoto'
        db.create_table('tool_toolphoto', (
            ('photo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['photo.Photo'], unique=True, primary_key=True)),
            ('tool', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tool.Tool'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=9999)),
        ))
        db.send_create_signal('tool', ['ToolPhoto'])

        # Adding model 'ToolLink'
        db.create_table('tool_toollink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tool', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tool.Tool'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=9999)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('tool', ['ToolLink'])

        # Deleting field 'Tool.src'
        db.delete_column('tool_tool', 'src')

        # Adding field 'Tool.thumbnail'
        db.add_column('tool_tool', 'thumbnail', self.gf('sorl.thumbnail.fields.ImageField')(max_length=300, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'ToolSlide'
        db.create_table('tool_toolslide', (
            ('tool', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tool.Tool'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=9999)),
            ('photo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['photo.Photo'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('tool', ['ToolSlide'])

        # Deleting model 'ToolVideo'
        db.delete_table('tool_toolvideo')

        # Deleting model 'ToolPhoto'
        db.delete_table('tool_toolphoto')

        # Deleting model 'ToolLink'
        db.delete_table('tool_toollink')

        # Adding field 'Tool.src'
        db.add_column('tool_tool', 'src', self.gf('sorl.thumbnail.fields.ImageField')(max_length=300, null=True, blank=True), keep_default=False)

        # Deleting field 'Tool.thumbnail'
        db.delete_column('tool_tool', 'thumbnail')


    models = {
        'article.article': {
            'Meta': {'ordering': "('-publish_date', 'title')", 'object_name': 'Article'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['auth.User']"}),
            'auto_tag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'feed_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'followup_for': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'followups'", 'blank': 'True', 'to': "orm['article.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['photo.Photo']", 'symmetrical': 'False', 'blank': 'True'}),
            'is_live': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'previous': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'next'", 'null': 'True', 'to': "orm['article.Article']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'related': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_rel_+'", 'blank': 'True', 'to': "orm['article.Article']"}),
            'rendered_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256', 'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['photo.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
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
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'src': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '300'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['auth.User']"})
        },
        'photo.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'project.project': {
            'Meta': {'ordering': "('-publish_date', 'title')", 'object_name': 'Project', '_ormbases': ['article.Article']},
            'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['article.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tool.lab': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Lab'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '9999'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'src': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        'tool.tool': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Tool'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tool.Lab']"}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '9999'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'thumbnail': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
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
            'Meta': {'ordering': "('order',)", 'object_name': 'ToolPhoto', '_ormbases': ['photo.Photo']},
            'order': ('django.db.models.fields.IntegerField', [], {'default': '9999'}),
            'photo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['photo.Photo']", 'unique': 'True', 'primary_key': 'True'}),
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
