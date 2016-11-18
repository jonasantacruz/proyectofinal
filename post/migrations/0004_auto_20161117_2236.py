# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-18 04:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.DateField(default=datetime.datetime(2016, 11, 18, 4, 36, 43, 857387, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
