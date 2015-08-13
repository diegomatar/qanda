# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0009_auto_20150805_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='follow_users',
            field=models.ManyToManyField(related_name='follow_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
