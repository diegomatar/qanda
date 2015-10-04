# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('perguntas', '0012_auto_20150925_1653'),
        ('notifications', '0009_noticomment_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotiAsk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unread', models.IntegerField(default=1, choices=[(1, b'unread'), (0, b'read')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('kind', models.CharField(default=b'ask_to_answer', max_length=50)),
                ('from_user', models.ManyToManyField(related_name='asknotif_from_user', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(to='perguntas.Pergunta')),
                ('to_user', models.ForeignKey(related_name='asknotif_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
