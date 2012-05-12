# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Assignment'
        db.create_table('chores_assignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('occurrence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chores.Occurrence'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('chores', ['Assignment'])

        # Adding model 'Completion'
        db.create_table('chores_completion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('occurrence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chores.Occurrence'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('chores', ['Completion'])

        # Deleting field 'Occurrence.due_date'
        db.delete_column('chores_occurrence', 'due_date')

        # Adding field 'Occurrence.datetime'
        db.add_column('chores_occurrence', 'datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 4, 1, 11, 8, 0, 575704)), keep_default=False)

        # Removing M2M table for field users on 'Occurrence'
        db.delete_table('chores_occurrence_users')


    def backwards(self, orm):
        
        # Deleting model 'Assignment'
        db.delete_table('chores_assignment')

        # Deleting model 'Completion'
        db.delete_table('chores_completion')

        # User chose to not deal with backwards NULL issues for 'Occurrence.due_date'
        raise RuntimeError("Cannot reverse this migration. 'Occurrence.due_date' and its values cannot be restored.")

        # Deleting field 'Occurrence.datetime'
        db.delete_column('chores_occurrence', 'datetime')

        # Adding M2M table for field users on 'Occurrence'
        db.create_table('chores_occurrence_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('occurrence', models.ForeignKey(orm['chores.occurrence'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('chores_occurrence_users', ['occurrence_id', 'user_id'])


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
        'chores.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'occurrence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chores.Occurrence']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'chores.completion': {
            'Meta': {'object_name': 'Completion'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'occurrence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chores.Occurrence']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'chores.occurrence': {
            'Meta': {'ordering': "('datetime',)", 'object_name': 'Occurrence'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chores.Task']"})
        },
        'chores.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'chores.task': {
            'Meta': {'object_name': 'Task'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'first_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'repeat': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['chores.Tag']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['chores']
