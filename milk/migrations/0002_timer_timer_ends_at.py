# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 20:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timer',
            name='timer_ends_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 17, 17, 52, 1, 31806)),
        ),
    ]
