# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perguntas', '0009_comment'),
        ('user_profile', '0011_userprofile_followers_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='interests',
            field=models.ManyToManyField(related_name='interests', to='perguntas.Tag'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='knows_about',
            field=models.ManyToManyField(related_name='knows_about', to='perguntas.Tag'),
        ),
    ]
