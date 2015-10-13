# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0018_userprofile_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='linkedin',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='google',
            field=models.URLField(null=True, verbose_name=b'Google', blank=True),
        ),
    ]
