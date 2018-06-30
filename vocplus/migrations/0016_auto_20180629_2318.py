# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-30 02:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vocplus', '0015_auto_20180629_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlearninglanguage',
            name='classification',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
        migrations.AddField(
            model_name='userlearninglanguage',
            name='last_access',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
