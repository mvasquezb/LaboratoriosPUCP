# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-20 00:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0008_auto_20170616_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratory',
            name='service_hours',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='internal.LaboratoryServiceHours'),
        ),
    ]
