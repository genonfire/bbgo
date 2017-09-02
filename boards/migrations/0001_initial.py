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
                ('status', models.CharField(default=b'1normal', max_length=10, choices=[(b'2temp', '\uc784\uc2dc\uc800\uc7a5'), (b'6deleted', '\uc0ad\uc81c\ub428'), (b'3notice', '\uacf5\uc9c0'), (b'5hidden', '\uad00\ub9ac\uc790 \uc0ad\uc81c'), (b'1normal', '\uc77c\ubc18'), (b'4warning', '\uc2e0\uace0\uc811\uc218')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField()),
                ('category', models.CharField(max_length=23, blank=True)),
                ('subject', models.CharField(max_length=41)),
                ('content', models.TextField()),
                ('view_count', models.IntegerField(default=0)),
                ('reply_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('dislike_count', models.IntegerField(default=0)),
                ('reference', models.CharField(default=b'', max_length=1855, blank=True)),
                ('dislike_users', models.ManyToManyField(related_name='board_dislike_users', to=settings.AUTH_USER_MODEL)),
                ('like_users', models.ManyToManyField(related_name='board_like_users', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article_id', models.IntegerField(default=0)),
                ('reply_id', models.IntegerField(default=0)),
                ('reply_to', models.CharField(default=b'', max_length=150, blank=True)),
                ('status', models.CharField(default=b'1normal', max_length=10, choices=[(b'6deleted', '\uc0ad\uc81c\ub428'), (b'5hidden', '\uad00\ub9ac\uc790 \uc0ad\uc81c'), (b'1normal', '\uc77c\ubc18')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField()),
                ('content', models.TextField(max_length=2000)),
                ('image', models.ImageField(upload_to=b'reply-images/%Y-%m-%d/', blank=True)),
                ('like_count', models.IntegerField(default=0)),
                ('dislike_count', models.IntegerField(default=0)),
                ('dislike_users', models.ManyToManyField(related_name='reply_dislike_users', to=settings.AUTH_USER_MODEL)),
                ('like_users', models.ManyToManyField(related_name='reply_like_users', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
