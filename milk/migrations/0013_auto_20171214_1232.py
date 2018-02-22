# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-14 12:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('milk', '0012_auto_20171130_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollChoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('choice_text', models.CharField(max_length=250)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PollQuestion',
            fields=[
                ('id', models.CharField(default='VXY6', max_length=4, primary_key=True, serialize=False)),
                ('question', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='timer',
            name='timer_ends_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 16, 32, 52, 650290)),
        ),
        migrations.AddField(
            model_name='pollchoice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='milk.PollQuestion'),
        ),
    ]