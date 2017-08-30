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
            name='Msg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sender_status', models.CharField(default=b'1normal', max_length=10, choices=[(b'6deleted', '\uc0ad\uc81c\ub428'), (b'1normal', '\uc77c\ubc18'), (b'5hidden', '\uc228\uae40')])),
                ('recipient_status', models.CharField(default=b'1normal', max_length=10, choices=[(b'6deleted', '\uc0ad\uc81c\ub428'), (b'1normal', '\uc77c\ubc18'), (b'5hidden', '\uc228\uae40')])),
                ('text', models.TextField(max_length=3000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField()),
                ('recipient', models.ForeignKey(related_name='msg_recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='msg_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
