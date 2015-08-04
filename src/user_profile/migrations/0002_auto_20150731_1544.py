# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 31, 18, 44, 31, 671961, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 31, 18, 44, 34, 424048, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
