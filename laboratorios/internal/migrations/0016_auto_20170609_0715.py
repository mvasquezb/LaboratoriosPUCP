# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0015_auto_20170608_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essaymethodparameterfill',
            name='uncertainty',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='essaymethodparameterfill',
            name='value',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
