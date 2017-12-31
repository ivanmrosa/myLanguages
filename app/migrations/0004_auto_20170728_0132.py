# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-28 01:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_sourcepagecategory_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegularExpression',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_regex_get_links', models.TextField(blank=True, null=True, verbose_name='Gravar uma lista python com os regex para pegar os links')),
                ('list_regex_get_title', models.TextField(verbose_name='Gravar uma lista python com os regex para pegar o titulo do artigo')),
                ('list_regex_get_article', models.TextField(verbose_name='Gravar uma lista python com os regex para o artigo')),
            ],
        ),
        migrations.RemoveField(
            model_name='sourcepagecategory',
            name='list_regex_get_article',
        ),
        migrations.RemoveField(
            model_name='sourcepagecategory',
            name='list_regex_get_links',
        ),
        migrations.RemoveField(
            model_name='sourcepagecategory',
            name='list_regex_get_title',
        ),
        migrations.AddField(
            model_name='sourcepagecategory',
            name='regular_expression',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.RegularExpression'),
        ),
    ]