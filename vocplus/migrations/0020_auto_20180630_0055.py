# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-30 03:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocplus', '0019_auto_20180630_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlearninglanguage',
            name='classification',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userlearninglanguage',
            name='last_access',
            field=models.DateField(blank=True, null=True),
        ),
    ]
