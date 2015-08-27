# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('perguntas', '0010_resposta_views'),
        ('user_profile', '0016_remove_userprofile_followers_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer_Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.IntegerField(choices=[(1, b'\xc3\x89 irritante ou desinteressante'), (2, b'Tem rela\xc3\xa7\xc3\xa3o comigo e n\xc3\xa3o gostei'), (3, b'Acho que n\xc3\xa3o deveria estar no QANDA'), (4, b'\xc3\x89 spam ou propaganda')])),
                ('status', models.IntegerField(default=1, choices=[(1, b'new'), (0, b'checked')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('classe', models.CharField(default=b'answer_report', max_length=100)),
                ('answer', models.ForeignKey(to='perguntas.Resposta')),
                ('from_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment_Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.IntegerField(choices=[(1, b'\xc3\x89 irritante ou desinteressante'), (2, b'Tem rela\xc3\xa7\xc3\xa3o comigo e n\xc3\xa3o gostei'), (3, b'Acho que n\xc3\xa3o deveria estar no QANDA'), (4, b'\xc3\x89 spam ou propaganda')])),
                ('status', models.IntegerField(default=1, choices=[(1, b'new'), (0, b'checked')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('classe', models.CharField(default=b'comment_report', max_length=100)),
                ('comment', models.ForeignKey(to='perguntas.Comment')),
                ('from_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile_Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.IntegerField(choices=[(1, b'\xc3\x89 irritante ou desinteressante'), (2, b'Tem rela\xc3\xa7\xc3\xa3o comigo e n\xc3\xa3o gostei'), (3, b'Acho que n\xc3\xa3o deveria estar no QANDA'), (4, b'\xc3\x89 spam ou propaganda')])),
                ('status', models.IntegerField(default=1, choices=[(1, b'new'), (0, b'checked')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('classe', models.CharField(default=b'profile_report', max_length=100)),
                ('from_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(to='user_profile.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Question_Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.IntegerField(choices=[(1, b'\xc3\x89 irritante ou desinteressante'), (2, b'Tem rela\xc3\xa7\xc3\xa3o comigo e n\xc3\xa3o gostei'), (3, b'Acho que n\xc3\xa3o deveria estar no QANDA'), (4, b'\xc3\x89 spam ou propaganda')])),
                ('status', models.IntegerField(default=1, choices=[(1, b'new'), (0, b'checked')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('classe', models.CharField(default=b'question_report', max_length=100)),
                ('from_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(to='perguntas.Pergunta')),
            ],
        ),
    ]
