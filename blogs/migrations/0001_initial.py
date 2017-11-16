# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'1normal', max_length=10, choices=[(b'2temp', 'status_draft'), (b'6deleted', '\uc0ad\uc81c\ub428'), (b'5hidden', 'status_pending'), (b'1normal', 'status_published')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField()),
                ('category', models.CharField(max_length=23, blank=True)),
                ('title', models.CharField(max_length=41)),
                ('content', models.TextField()),
                ('view_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('like_users', models.TextField(default=b'', blank=True)),
                ('image', models.ImageField(upload_to=b'featured_images/%Y-%m/', blank=True)),
                ('tags', models.TextField(default=b'', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_id', models.IntegerField(default=0)),
                ('comment_id', models.IntegerField(default=0)),
                ('status', models.CharField(default=b'1normal', max_length=10, choices=[(b'6deleted', '\uc0ad\uc81c\ub428'), (b'7spam', 'status_spam'), (b'1normal', '\uc77c\ubc18')])),
                ('userid', models.CharField(max_length=16, blank=True)),
                ('username', models.CharField(max_length=23, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField()),
                ('content', models.TextField(max_length=2000)),
            ],
        ),
    ]
