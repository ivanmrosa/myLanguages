# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-14 01:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vocplus', '0004_auto_20180113_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sequence', models.IntegerField()),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocplus.Language')),
            ],
            options={
                'ordering': ['sequence'],
                'db_table': 'Lesson',
            },
        ),
    ]