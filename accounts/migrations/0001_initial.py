# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import accounts.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('point', models.IntegerField(default=1)),
                ('last_article_at', models.DateTimeField(auto_now_add=True)),
                ('last_reply_at', models.DateTimeField(auto_now_add=True)),
                ('bookmarks', models.TextField(default=b'', blank=True)),
                ('scrap', models.TextField(default=b'', blank=True)),
                ('alarm', models.BooleanField(default=False)),
                ('msg_count', models.IntegerField(default=0)),
                ('alarm_list', models.TextField(default=b'', blank=True)),
                ('ip_list', models.TextField(default=b'', blank=True)),
                ('sense_client', models.CharField(max_length=30, blank=True)),
                ('sense_slot', models.CharField(max_length=15, blank=True)),
                ('portrait', models.ImageField(blank=True, upload_to=b'portrait/%Y-%m-%d/', validators=[accounts.models.img_validator])),
                ('signature', models.TextField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
