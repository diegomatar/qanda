# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20150807_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notivote',
            name='answer',
            field=models.ForeignKey(related_name='answer', blank=True, to='perguntas.Resposta', null=True),
        ),
    ]
