# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_auto_20150804_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='about',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='facebook',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='linkedin',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='twitter',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
