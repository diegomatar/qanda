# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0014_auto_20150822_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='follow_users',
            field=models.ManyToManyField(related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
    ]
