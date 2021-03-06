# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-14 12:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vocplus', '0008_language_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserComplement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('official_language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocplus.Language')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserComplement',
            },
        ),
        migrations.CreateModel(
            name='UserLearningLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('actual_lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocplus.Lesson')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocplus.Language')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserLearningLanguage',
            },
        ),
    ]
