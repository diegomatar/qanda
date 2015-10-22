# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0020_userbio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbio',
            name='bio',
            field=models.CharField(default='teste', max_length=200, verbose_name=b'Sobre'),
            preserve_default=False,
        ),
    ]
