# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-26 09:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0014_auto_20170623_0054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleinventory',
            name='expiration_date',
        ),
    ]