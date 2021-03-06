# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-21 04:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0009_auto_20170619_1928'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('quantity', models.PositiveIntegerField()),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InventoryArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('inventoryarticle_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='internal.InventoryArticle')),
                ('servicelife_unit', models.CharField(max_length=50)),
                ('servicelife', models.PositiveIntegerField()),
                ('error_range', models.FloatField()),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('internal.inventoryarticle',),
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('inventoryarticle_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='internal.InventoryArticle')),
                ('metric_unit', models.PositiveIntegerField()),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('internal.inventoryarticle',),
        ),
        migrations.AddField(
            model_name='articleinventory',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.InventoryArticle'),
        ),
        migrations.AddField(
            model_name='articleinventory',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Inventory'),
        ),
    ]
