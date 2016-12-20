# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import wmd.models
import membership.models


class Migration(migrations.Migration):

    dependencies = [
        ('drop', '0001_initial'),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('status', models.CharField(default=b'used', help_text=b'Automatically set when changes are made to subscription or container via admin.', max_length=16, choices=[(b'used', b'Used'), (b'staff', b'Staff'), (b'canceled', b'Needs Email'), (b'emailed', b'Emailed'), (b'maintenance', b'Maintenance'), (b'open', b'Open')])),
                ('kind', models.CharField(default=b'bay', max_length=64, choices=[(b'drawer', b'Drawer'), (b'table', b'Table'), (b'bay', b'Bay'), (b'studio', b'Studio')])),
                ('notes', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('room', 'number'),
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ('text',),
            },
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=64, choices=[(b'recurring_payment_skipped', b'PayPal Skipped'), (b'recurring_payment_failed', b'PayPal Failed Recurring'), (b'recurring_payment_suspended', b'PayPal Suspended'), (b'recurring_payment_suspended_due_to_max_failed_payment', b'PayPal Max Failed Payment'), (b'subscr_failed', b'PayPal Failed Subscription'), (b'subscr_eot', b'PayPal End of Term'), (b'manually_flagged', b'Manually Flagged'), (b'safety', b'Expiring Safety Criterion')])),
                ('status', models.CharField(default=b'new', max_length=32, choices=[(b'new', b'New'), (b'first_warning', b'Warned Once'), (b'second_warning', b'Warned Twice'), (b'final_warning', b'Canceled (Automatically)'), (b'canceled', b'Canceled (Manually)'), (b'resolved', b'Resolved'), (b'paid', b'Paid'), (b'safety_new', b'New'), (b'safety_emailed', b'Emailed'), (b'safety_expired', b'Expired (criterion revoked)'), (b'safety_completed', b'Completed (course taken)')])),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('emailed', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('order', models.IntegerField(verbose_name=b'Level')),
                ('discount_percentage', models.IntegerField(default=0)),
                ('permission_description', models.TextField(default=b'', blank=True)),
                ('machine_credits', models.IntegerField(default=0)),
                ('simultaneous_users', models.IntegerField(default=0)),
                ('cost_per_credit', models.DecimalField(default=0, max_digits=30, decimal_places=2)),
                ('custom_training_cost', models.DecimalField(default=0, max_digits=30, decimal_places=2)),
                ('custom_training_max', models.DecimalField(default=0, max_digits=30, decimal_places=2)),
                ('holiday_access', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Membership Level',
            },
        ),
        migrations.CreateModel(
            name='LevelDoorGroupSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ('level',),
            },
        ),
        migrations.CreateModel(
            name='LimitedAccessKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=32)),
                ('created', models.DateField(auto_now_add=True)),
                ('expires', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MeetingMinutes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.date.today, unique=True)),
                ('content', wmd.models.MarkDownField()),
                ('member_count', models.IntegerField(default=0, help_text=b'Used only when an exact list of members is unavailable (eg legacy minutes)')),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='MembershipFeature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Officer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.CharField(max_length=50)),
                ('start', models.DateField(default=datetime.date.today)),
                ('end', models.DateField(null=True, blank=True)),
                ('order', models.IntegerField(default=999)),
            ],
            options={
                'ordering': ('order', 'end'),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='drop.Product')),
                ('months', models.IntegerField(default=1, choices=[(1, b'Monthly'), (3, b'Quarterly'), (6, b'Biannually'), (12, b'Yearly')])),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=('drop.product',),
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=256, null=True, blank=True)),
                ('original', wmd.models.MarkDownField()),
                ('ammended', wmd.models.MarkDownField(null=True, blank=True)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0, max_digits=30, decimal_places=2)),
                ('payment_method', models.CharField(default=b'cash', max_length=16, choices=[(b'paypal', b'PayPalIPN'), (b'cash', b'Cash/Check'), (b'adjustment', b'Adjustment (gift from lab)'), (b'refund', b'Refund'), (b'legacy', b'Legacy (PayPal)')])),
                ('notes', models.CharField(max_length=128, null=True, blank=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('transaction_id', models.CharField(max_length=32, null=True, blank=True)),
            ],
            options={
                'ordering': ('datetime',),
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subscr_id', models.CharField(help_text=b'Only used with PayPal subscriptions. Do not touch.', max_length=20, null=True, blank=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('canceled', models.DateTimeField(null=True, blank=True)),
                ('paid_until', models.DateTimeField(null=True, blank=True)),
                ('amount', models.DecimalField(default=0, max_digits=30, decimal_places=2)),
                ('owed', models.DecimalField(default=0, max_digits=30, decimal_places=2)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reasons', models.TextField(blank=True)),
                ('projects', models.TextField(blank=True)),
                ('skills', models.TextField(blank=True)),
                ('expertise', models.TextField(blank=True)),
                ('questions', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnsubscribeLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=32)),
                ('created', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voting_rights', models.BooleanField(default=False)),
                ('suspended', models.BooleanField(default=False)),
                ('bio', wmd.models.MarkDownField(null=True, blank=True)),
                ('api_key', models.CharField(default=membership.models.rand32, max_length=32)),
                ('by_line', models.CharField(help_text=b'A short description of what you do for the lab.', max_length=50, null=True, blank=True)),
                ('notify_global', models.BooleanField(default=True, help_text=b'Uncheck this to stop all email correspondance from this website (same as unchecking all the below items and any future notifications we add).', verbose_name=b'Global Email Preference')),
                ('notify_comments', models.BooleanField(default=True, help_text=b'If checked, you will be emailed whenever someone replies to a comment you make on this site.', verbose_name=b'Comment Response Email')),
                ('notify_classes', models.BooleanField(default=True, help_text=b"If checked, you will be emailed a reminder 24 hours before a class (that you've signed up for).", verbose_name=b'Class Reminder Email')),
                ('notify_sessions', models.BooleanField(default=True, help_text=b'If checked, you will be emailed new class offerings (twice a month).', verbose_name=b'New Course Email')),
                ('photo', models.ForeignKey(blank=True, to='media.Photo', null=True)),
            ],
        ),
    ]
