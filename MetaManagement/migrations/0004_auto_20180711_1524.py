# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-07-11 07:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MetaManagement', '0003_auto_20180711_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='is_fetched',
            field=models.BooleanField(default=False, verbose_name='Blob Fetched'),
        ),
    ]
