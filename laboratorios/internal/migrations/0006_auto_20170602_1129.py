# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 16:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0005_auto_20170601_2250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='essaytemplate',
            old_name='name',
            new_name='description',
        ),
    ]