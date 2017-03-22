# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20170213_0507'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='table',
            field=models.CharField(default=b'1', max_length=b'30', choices=[(b'0', b'default'), (b'1', b'test')]),
        ),
    ]
