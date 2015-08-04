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
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'profile_pictures')),
                ('points', models.IntegerField(default=0)),
                ('perg_downvotes', models.ManyToManyField(related_name='perg_downvotes', to='perguntas.Pergunta')),
                ('perg_upvotes', models.ManyToManyField(related_name='perg_upvotes', to='perguntas.Pergunta')),
                ('resp_downvotes', models.ManyToManyField(related_name='resp_downvotes', to='perguntas.Resposta')),
                ('resp_upvotes', models.ManyToManyField(related_name='resp_upvotes', to='perguntas.Resposta')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
