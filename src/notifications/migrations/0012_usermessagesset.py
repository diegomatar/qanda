# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0011_auto_20150928_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMessagesSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('new_follower', models.BooleanField()),
                ('follow_activities', models.BooleanField()),
                ('answer_question', models.BooleanField()),
                ('question_in_tag', models.BooleanField()),
                ('ask_answer', models.BooleanField()),
                ('new_comment', models.BooleanField()),
                ('new_vote', models.BooleanField()),
                ('email_summary_day', models.BooleanField()),
                ('email_summary_week', models.BooleanField()),
            ],
        ),
    ]
