# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-30 03:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0022_auto_20170629_2249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extrarequestconcept',
            old_name='request',
            new_name='quotation',
        ),
    ]
