# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-30 03:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vocplus', '0018_auto_20180630_0008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlearninglanguage',
            name='classification',
        ),
        migrations.RemoveField(
            model_name='userlearninglanguage',
            name='last_access',
        ),
    ]
