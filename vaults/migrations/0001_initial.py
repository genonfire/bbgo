# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import fernet_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('masterkey', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expiry', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Vault',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=1)),
                ('category', models.CharField(default=b'account', max_length=12, choices=[(b'account', '\uacc4\uc88c'), (b'card', '\uce74\ub4dc'), (b'membership', '\uba64\ubc84\uc2ed'), (b'other', '\uae30\ud0c0')])),
                ('name', fernet_fields.fields.EncryptedCharField(max_length=23)),
                ('number', fernet_fields.fields.EncryptedCharField(max_length=64)),
                ('valid', fernet_fields.fields.EncryptedCharField(max_length=20, blank=True)),
                ('cvc', fernet_fields.fields.EncryptedCharField(max_length=10, blank=True)),
                ('description', fernet_fields.fields.EncryptedCharField(max_length=128, blank=True)),
                ('image', models.ImageField(upload_to=b'vaults/', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
    ]
