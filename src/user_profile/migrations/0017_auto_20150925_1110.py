# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perguntas', '0010_resposta_views'),
        ('user_profile', '0016_remove_userprofile_followers_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='follow_questions',
            field=models.ManyToManyField(related_name='follow_questions', to='perguntas.Pergunta'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='follow_topics',
            field=models.ManyToManyField(related_name='follow_topics', to='perguntas.Tag'),
        ),
    ]
