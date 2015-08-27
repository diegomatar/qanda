# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0013_userprofile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='follow_users',
            field=models.ManyToManyField(related_name='follow_users1', to=settings.AUTH_USER_MODEL),
        ),
    ]
