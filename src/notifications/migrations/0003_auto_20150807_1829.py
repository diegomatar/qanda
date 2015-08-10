# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20150807_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='notianswer',
            name='kind',
            field=models.CharField(default=b'answer', max_length=50),
        ),
        migrations.AddField(
            model_name='notianswer',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 21, 28, 55, 63625, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notianswer',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 21, 28, 57, 903882, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notivote',
            name='kind',
            field=models.CharField(default=b'vote', max_length=50),
        ),
        migrations.AddField(
            model_name='notivote',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 21, 29, 0, 535911, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notivote',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 21, 29, 2, 815911, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
