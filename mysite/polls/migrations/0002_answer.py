# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 06:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0001_initial'),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_id', models.IntegerField()),
                ('question_id', models.IntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanager.PollUser')),
            ],
        ),
    ]
