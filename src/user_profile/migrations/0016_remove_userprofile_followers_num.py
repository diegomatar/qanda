# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0015_auto_20150822_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='followers_num',
        ),
    ]
