# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('codrspace_miscfile', 'media_miscfile') 
        db.rename_table('codrspace_photo', 'media_photo') 
        db.rename_table('codrspace_photo_tags', 'media_photo_tags') 
        db.rename_table('codrspace_phototag', 'media_phototag') 
        db.rename_table('codrspace_taggedphoto', 'media_taggedphoto')
        db.rename_table('codrspace_taggedfile', 'media_taggedfile')
        # Changing field 'Post.photo'
        db.alter_column(u'codrspace_post', 'photo_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media.Photo'], null=True))

        if not db.dry_run:
            # For permissions to work properly after migrating
            orm['contenttypes.contenttype'].objects.filter(app_label='codrspace', model='miscfile').update(app_label='media')
            orm['contenttypes.contenttype'].objects.filter(app_label='codrspace', model='photo').update(app_label='media')
            orm['contenttypes.contenttype'].objects.filter(app_label='codrspace', model='phototag').update(app_label='media')
            orm['contenttypes.contenttype'].objects.filter(app_label='codrspace', model='taggedphoto').update(app_label='media')
            orm['contenttypes.contenttype'].objects.filter(app_label='codrspace', model='taggedfile').update(app_label='media')

    def backwards(self, orm):
        db.rename_table('media_miscfile', 'codrspace_miscfile') 
        db.rename_table('media_photo', 'codrspace_photo') 
        db.rename_table('media_photo_tags', 'codrspace_photo_tags') 
        db.rename_table('media_phototag', 'codrspace_phototag') 
        db.rename_table('media_taggedphoto', 'codrspace_taggedphoto')
        db.rename_table('media_taggedfile', 'codrspace_taggedfile')
        # Changing field 'Post.photo'
        db.alter_column(u'media_post', 'photo_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['codrspace.Photo'], null=True))

        if not db.dry_run:
            # For permissions to work properly after migrating
            orm['contenttypes.contenttype'].objects.filter(app_label='media', model='miscfile').update(app_label='codrspace')
            orm['contenttypes.contenttype'].objects.filter(app_label='media', model='photo').update(app_label='codrspace')
            orm['contenttypes.contenttype'].objects.filter(app_label='media', model='phototag').update(app_label='codrspace')
            orm['contenttypes.contenttype'].objects.filter(app_label='media', model='taggedphoto').update(app_label='codrspace')
            orm['contenttypes.contenttype'].objects.filter(app_label='media', model='taggedfile').update(app_label='codrspace')



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
        u'codrspace.banner': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Banner'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'header': ('django.db.models.fields.CharField', [], {'default': "'Featured Event'", 'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'src': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        },
        u'codrspace.post': {
            'Meta': {'ordering': "('-featured', '-publish_dt')", 'unique_together': "(('slug', 'user'),)", 'object_name': 'Post'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'create_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['media.Photo']", 'null': 'True', 'blank': 'True'}),
            'publish_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'short_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '75'}),
            'status': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '30'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'update_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'codrspace.pressitem': {
            'Meta': {'ordering': "('-publish_dt',)", 'object_name': 'PressItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_dt': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '256'})
        },
        u'codrspace.profile': {
            'Meta': {'object_name': 'Profile'},
            'git_access_token': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'codrspace.setting': {
            'Meta': {'object_name': 'Setting'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'blog_tagline': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'blog_title': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'timezone': ('timezones.fields.TimeZoneField', [], {'default': "'US/Central'", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'instagram.instagramlocation': {
            'Meta': {'object_name': 'InstagramLocation'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'follow': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'instagram.instagramphoto': {
            'Meta': {'ordering': "('-created_time',)", 'object_name': 'InstagramPhoto'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'instagram_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['instagram.InstagramLocation']", 'null': 'True', 'blank': 'True'}),
            'instagram_tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['instagram.InstagramTag']", 'null': 'True', 'blank': 'True'}),
            'instagram_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['instagram.InstagramUser']", 'null': 'True', 'blank': 'True'}),
            'low_resolution': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rejected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'standard_resolution': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'instagram.instagramtag': {
            'Meta': {'object_name': 'InstagramTag'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'follow': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'instagram.instagramuser': {
            'Meta': {'object_name': 'InstagramUser'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'follow': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'profile_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'media.photo': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Photo'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'external_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'file': ('crop_override.field.OriginalImage', [], {'max_length': '200', 'null': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagramphoto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['instagram.InstagramPhoto']", 'null': 'True', 'blank': 'True'}),
            'landscape_crop': ('crop_override.field.CropOverride', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'portrait_crop': ('crop_override.field.CropOverride', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'web'", 'max_length': '16'}),
            'square_crop': ('crop_override.field.CropOverride', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['media.PhotoTag']", 'symmetrical': 'False', 'blank': 'True'}),
            'upload_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'media.phototag': {
            'Meta': {'ordering': "('-name',)", 'object_name': 'PhotoTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['codrspace']
