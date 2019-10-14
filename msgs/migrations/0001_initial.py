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
                ('sender_status', models.CharField(default=b'1normal', max_length=10, choices=[(b'6deleted', '\uc0ad\uc81c\ub428'), (b'5hidden', '\uad00\ub9ac\uc790 \uc0ad\uc81c'), (b'1normal', '\uc77c\ubc18'), (b'2read', '\uc77d\uc74c')])),
                ('recipient_status', models.CharField(default=b'1normal', max_length=10, choices=[(b'6deleted', '\uc0ad\uc81c\ub428'), (b'5hidden', '\uad00\ub9ac\uc790 \uc0ad\uc81c'), (b'1normal', '\uc77c\ubc18'), (b'2read', '\uc77d\uc74c')])),
                ('text', models.TextField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField()),
                ('recipient', models.ForeignKey(related_name='msg_recipient', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('sender', models.ForeignKey(related_name='msg_sender', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
    ]
