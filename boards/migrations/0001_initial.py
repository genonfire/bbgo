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
                ('table', models.IntegerField(default=0)),
                ('status', models.CharField(default=b'1normal', max_length=10, choices=[('1normal', '\uc815\uc0c1'), ('2temp', '\uc784\uc2dc\uc800\uc7a5'), ('6deleted', '\uc0ad\uc81c\ub428'), ('3notice', '\uacf5\uc9c0'), ('5hidden', '\uc228\uae40'), ('4warning', '\uc2e0\uace0\uc811\uc218')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('ip', models.GenericIPAddressField()),
                ('category', models.CharField(max_length=23, blank=True)),
                ('subject', models.CharField(max_length=41)),
                ('content', models.TextField()),
                ('view_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('dislike_count', models.IntegerField(default=0)),
                ('reply_count', models.IntegerField(default=0)),
                ('like_users', models.TextField(default=b'', blank=True)),
                ('dislike_users', models.TextField(default=b'', blank=True)),
                ('replies', models.TextField(default=b'', blank=True)),
                ('reference', models.CharField(default=b'', max_length=1855, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
