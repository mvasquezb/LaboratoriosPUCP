# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 04:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('idDoc', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RoleByAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Access')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Role')),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=30)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Request')),
            ],
        ),
        migrations.CreateModel(
            name='SampleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Request')),
            ],
        ),
        migrations.CreateModel(
            name='TestFill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Request')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='TestType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('userDescription', models.CharField(max_length=200, null=True)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserByRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.User')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ManyToManyField(through='internal.UserByRole', to='internal.Role'),
        ),
        migrations.AddField(
            model_name='testfill',
            name='testType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.TestType'),
        ),
        migrations.AddField(
            model_name='sample',
            name='sampleType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.SampleType'),
        ),
        migrations.AddField(
            model_name='role',
            name='access',
            field=models.ManyToManyField(through='internal.RoleByAccess', to='internal.Access'),
        ),
        migrations.AddField(
            model_name='client',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='internal.User'),
        ),
    ]