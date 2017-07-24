# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='reply_to',
            field=models.CharField(default=b'', max_length=150, blank=True),
        ),
    ]
