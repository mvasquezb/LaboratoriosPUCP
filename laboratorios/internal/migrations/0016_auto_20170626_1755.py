# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-26 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0015_remove_articleinventory_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalprovider',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
