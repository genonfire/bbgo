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
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('table', models.IntegerField(default=0)),
                ('status', models.CharField(default=b'1normal', max_length=10, choices=[(b'6deleted', '\uc0ad\uc81c\ub428'), (b'7canceled', '\ucde8\uc18c'), (b'5hidden', '\uad00\ub9ac\uc790 \uc0ad\uc81c'), (b'1normal', '\uc77c\ubc18'), (b'8full', '\ub9c8\uac10')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField()),
                ('category', models.CharField(max_length=23, blank=True)),
                ('subject', models.CharField(max_length=41)),
                ('content', models.TextField(default=b'', blank=True)),
                ('view_count', models.IntegerField(default=0)),
                ('reply_count', models.IntegerField(default=0)),
                ('slot', models.IntegerField(default=1)),
                ('slot_total', models.IntegerField(default=6)),
                ('slot_users', models.ManyToManyField(related_name='team_slot_users', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='TeamReply',
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
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
    ]
