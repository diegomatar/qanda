# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20150807_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notianswer',
            name='unread',
            field=models.IntegerField(default=1, choices=[(1, b'unread'), (0, b'read')]),
        ),
        migrations.AlterField(
            model_name='notivote',
            name='question',
            field=models.ForeignKey(blank=True, to='perguntas.Pergunta', null=True),
        ),
        migrations.AlterField(
            model_name='notivote',
            name='unread',
            field=models.IntegerField(default=1, choices=[(1, b'unread'), (0, b'read')]),
        ),
        migrations.AlterField(
            model_name='notivote',
            name='vote',
            field=models.IntegerField(default=1, choices=[(1, b'like'), (0, b'unlike')]),
        ),
    ]
