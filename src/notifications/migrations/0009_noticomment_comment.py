# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perguntas', '0010_resposta_views'),
        ('notifications', '0008_auto_20150829_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticomment',
            name='comment',
            field=models.ForeignKey(blank=True, to='perguntas.Comment', null=True),
        ),
    ]
