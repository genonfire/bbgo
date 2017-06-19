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
            name='Board',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('table', models.CharField(default=b'0', max_length=b'31', choices=[(b'0', b'default'), (b'1', b'test')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(blank=True)),
                ('ip', models.GenericIPAddressField()),
                ('category', models.CharField(max_length=20, blank=True)),
                ('subject', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('view_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('dislike_count', models.IntegerField(default=0)),
                ('reply_count', models.IntegerField(default=0)),
                ('like_users', models.TextField(default=b'', blank=True)),
                ('dislike_users', models.TextField(default=b'', blank=True)),
                ('replies', models.TextField(default=b'', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
