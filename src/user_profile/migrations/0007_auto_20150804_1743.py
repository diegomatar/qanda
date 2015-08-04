# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_auto_20150804_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='about',
            field=models.TextField(max_length=500, null=True, verbose_name=b'Sobre', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=254, verbose_name=b'email'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='facebook',
            field=models.URLField(null=True, verbose_name=b'Facebook', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=30, null=True, verbose_name=b'Nome', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=30, null=True, verbose_name=b'Sobrenome', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='linkedin',
            field=models.URLField(null=True, verbose_name=b'Linked In', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(upload_to=b'profile_pictures', verbose_name=b'Imagem de Perfil'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='twitter',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Twitter', blank=True),
        ),
    ]
