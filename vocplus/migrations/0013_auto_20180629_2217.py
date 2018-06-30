# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-30 01:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocplus', '0012_userlearninglanguage_classification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlearninglanguage',
            name='classification',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='userlearninglanguage',
            name='last_access',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 6, 29, 22, 17, 7, 179539), null=True),
        ),
    ]
