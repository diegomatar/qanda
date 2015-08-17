# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('perguntas', '0009_comment'),
        ('notifications', '0006_notifollow'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotiComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unread', models.IntegerField(default=1, choices=[(1, b'unread'), (0, b'read')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('kind', models.CharField(default=b'comment', max_length=50)),
                ('answer', models.ForeignKey(to='perguntas.Resposta')),
                ('from_user', models.ForeignKey(related_name='cnotif_from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(related_name='cnotif_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
