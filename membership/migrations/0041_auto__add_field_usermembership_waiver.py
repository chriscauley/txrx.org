# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserMembership.waiver'
        db.add_column(u'membership_usermembership', 'waiver',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserMembership.waiver'
        db.delete_column(u'membership_usermembership', 'waiver')


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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.User']", 'null': 'True', 'blank': 'True'}),
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.User']", 'null': 'True', 'blank': 'True'})
        },
        u'media.phototag': {
            'Meta': {'ordering': "('-name',)", 'object_name': 'PhotoTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'membership.feature': {
            'Meta': {'ordering': "('text',)", 'object_name': 'Feature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'membership.limitedaccesskey': {
            'Meta': {'object_name': 'LimitedAccessKey'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.User']"})
        },
        u'membership.meetingminutes': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'MeetingMinutes'},
            'content': ('wmd.models.MarkDownField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inactive_present': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'meetings_inactive'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['user.User']"}),
            'member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nonvoters_present': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['user.User']"}),
            'voters_present': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['user.User']", 'null': 'True', 'blank': 'True'})
        },
        u'membership.membership': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Membership'},
            'discount_percentage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membershipgroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['membership.MembershipGroup']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        u'membership.membershipfeature': {
            'Meta': {'ordering': "('order',)", 'object_name': 'MembershipFeature'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['membership.Feature']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['membership.Membership']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'membership.membershipgroup': {
            'Meta': {'ordering': "('order',)", 'object_name': 'MembershipGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'membership.membershiprate': {
            'Meta': {'ordering': "('order',)", 'object_name': 'MembershipRate'},
            'cost': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['membership.Membership']"}),
            'months': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'membership.officer': {
            'Meta': {'ordering': "('order', 'end')", 'object_name': 'Officer'},
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '999'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.User']"})
        },
        u'membership.proposal': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Proposal'},
            'ammended': ('wmd.models.MarkDownField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting_minutes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['membership.MeetingMinutes']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'original': ('wmd.models.MarkDownField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.User']"})
        },
        u'membership.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'membership.survey': {
            'Meta': {'object_name': 'Survey'},
            'expertise': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projects': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'questions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reasons': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'skills': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.User']", 'unique': 'True'})
        },
        u'membership.unsubscribelink': {
            'Meta': {'object_name': 'UnsubscribeLink'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.User']"})
        },
        u'membership.usermembership': {
            'Meta': {'object_name': 'UserMembership'},
            'api_key': ('django.db.models.fields.CharField', [], {'default': "'69ZvJb1lsvFWoE0qv8Ti7PKRfIlRzxDq'", 'max_length': '32'}),
            'bio': ('wmd.models.MarkDownField', [], {'null': 'True', 'blank': 'True'}),
            'by_line': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['membership.Membership']"}),
            'notify_classes': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_global': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_sessions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'paypal_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['media.Photo']", 'null': 'True', 'blank': 'True'}),
            'suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['user.User']", 'unique': 'True'}),
            'voting_rights': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'waiver': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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

    complete_apps = ['membership']