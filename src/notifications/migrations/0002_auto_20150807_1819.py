# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notianswer',
            old_name='user',
            new_name='to_user',
        ),
        migrations.RenameField(
            model_name='notivote',
            old_name='user',
            new_name='to_user',
        ),
    ]
