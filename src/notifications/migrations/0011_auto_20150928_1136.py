# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0010_notiask'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notiask',
            name='from_user',
        ),
        migrations.AddField(
            model_name='notiask',
            name='from_user',
            field=models.ForeignKey(related_name='asknotif_from_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
