# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perguntas', '0010_resposta_views'),
        ('notifications', '0007_noticomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='notianswer',
            name='answer',
            field=models.ForeignKey(related_name='anotif_answer', blank=True, to='perguntas.Resposta', null=True),
        ),
        migrations.AlterField(
            model_name='notianswer',
            name='question',
            field=models.ForeignKey(related_name='anotif_question', to='perguntas.Pergunta'),
        ),
    ]
