# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-21 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0010_auto_20170620_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='supply',
            name='metric_unit',
            field=models.CharField(max_length=20),
        ),
    ]
