# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0017_auto_20150925_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_role',
            field=models.CharField(default=b'regular', max_length=50, choices=[(b'regular', b'regular'), (b'editor', b'editor'), (b'admin', b'admin')]),
        ),
    ]
