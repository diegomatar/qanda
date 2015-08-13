# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0005_auto_20150810_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotiFollow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unread', models.IntegerField(default=1, choices=[(1, b'unread'), (0, b'read')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('kind', models.CharField(default=b'follow', max_length=50)),
                ('from_user', models.ForeignKey(related_name='fnotif_from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(related_name='fnotif_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
