# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('perguntas', '0007_auto_20150731_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotiAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unread', models.IntegerField(default=1, choices=[(b'unread', 1), (b'read', 0)])),
                ('from_user', models.ForeignKey(related_name='anotif_from_user', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(related_name='question', to='perguntas.Pergunta')),
                ('user', models.ForeignKey(related_name='anotif_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotiVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unread', models.IntegerField(default=1, choices=[(b'unread', 1), (b'read', 0)])),
                ('vote', models.IntegerField(default=1, choices=[(b'like', 1), (b'unlike', 0)])),
                ('answer', models.ForeignKey(related_name='answer', blank=True, to='perguntas.Pergunta', null=True)),
                ('from_user', models.ForeignKey(related_name='vnotif_from_user', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(to='perguntas.Pergunta', blank=True)),
                ('user', models.ForeignKey(related_name='vnotif_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
