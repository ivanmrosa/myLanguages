# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-14 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocplus', '0007_lessonmedia'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
