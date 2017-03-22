# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='likecount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='board',
            name='category',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='board',
            name='likeusers',
            field=models.TextField(default=b''),
        ),
    ]
