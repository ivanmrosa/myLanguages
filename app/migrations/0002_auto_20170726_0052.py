# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-26 00:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcepagecategory',
            name='list_regex_get_article',
            field=models.TextField(default='', verbose_name='Gravar uma lista python com os regex para o artigo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sourcepagecategory',
            name='list_regex_get_links',
            field=models.TextField(blank=True, null=True, verbose_name='Gravar uma lista python com os regex para pegar os links'),
        ),
        migrations.AddField(
            model_name='sourcepagecategory',
            name='list_regex_get_title',
            field=models.TextField(default='', verbose_name='Gravar uma lista python com os regex para pegar o titulo do artigo'),
            preserve_default=False,
        ),
    ]