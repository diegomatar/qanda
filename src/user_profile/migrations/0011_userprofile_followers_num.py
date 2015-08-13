# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0010_userprofile_follow_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='followers_num',
            field=models.IntegerField(default=0),
        ),
    ]
