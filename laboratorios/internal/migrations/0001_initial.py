# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-14 21:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import internal.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Essay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EssayFill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
                ('essay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Essay')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EssayMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EssayMethodFill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('chosen', models.BooleanField(default=False)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
                ('essay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.EssayFill')),
                ('essay_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='essay_methods', to='internal.EssayMethod')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EssayMethodParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('description', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=20)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EssayMethodParameterFill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('value', models.CharField(blank=True, max_length=20, null=True)),
                ('uncertainty', models.FloatField(blank=True, null=True)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
                ('essay_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='internal.EssayMethodFill')),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.EssayMethodParameter')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExternalProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExternalProviderService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('description', models.CharField(max_length=500)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InventoryItem',
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
            name='InventoryOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('unsettled', models.BooleanField()),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
                ('essay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.EssayFill')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InventoryOrderDefault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('detail', models.CharField(max_length=100)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('capacity', models.PositiveIntegerField()),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
                ('essay_methods', models.ManyToManyField(blank=True, related_name='laboratories', to='internal.EssayMethod')),
                ('inventory', models.ManyToManyField(blank=True, related_name='laboratories', to='internal.Inventory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LaboratoryServiceHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('start_time', models.PositiveIntegerField()),
                ('end_time', models.PositiveIntegerField()),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RequestAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('fileName', models.CharField(max_length=100, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=internal.models.content_file_name)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
                ('permissions', models.ManyToManyField(blank=True, to='auth.Permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(default='default', max_length=50)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Inventory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SampleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('slug', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceContractModification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('description', models.CharField(max_length=100)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.ServiceContract')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('observations', models.CharField(blank=True, max_length=500, null=True)),
                ('expected_duration', models.IntegerField(default=10)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceRequestState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('slug', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=20)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('basicuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='internal.BasicUser')),
                ('code', models.CharField(max_length=10)),
                ('doc_number', models.IntegerField()),
                ('phone_number', models.CharField(max_length=20)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('internal.basicuser',),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('basicuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='internal.BasicUser')),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('internal.basicuser',),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.ServiceRequestState'),
        ),
        migrations.AddField(
            model_name='servicecontract',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.ServiceRequest'),
        ),
        migrations.AddField(
            model_name='sample',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.ServiceRequest'),
        ),
        migrations.AddField(
            model_name='sample',
            name='sample_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.SampleType'),
        ),
        migrations.AddField(
            model_name='requestattachment',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.ServiceRequest'),
        ),
        migrations.AddField(
            model_name='quotation',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.ServiceRequest'),
        ),
        migrations.AddField(
            model_name='laboratory',
            name='service_hours',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.LaboratoryServiceHours'),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Sample'),
        ),
        migrations.AddField(
            model_name='externalprovider',
            name='services',
            field=models.ManyToManyField(blank=True, to='internal.ExternalProviderService'),
        ),
        migrations.AddField(
            model_name='essaymethodfill',
            name='external_provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='internal.ExternalProvider'),
        ),
        migrations.AddField(
            model_name='essaymethodfill',
            name='inventory_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='internal.InventoryOrder'),
        ),
        migrations.AddField(
            model_name='essaymethod',
            name='parameters',
            field=models.ManyToManyField(blank=True, related_name='essaymethods', to='internal.EssayMethodParameter'),
        ),
        migrations.AddField(
            model_name='essaymethod',
            name='sample_types',
            field=models.ManyToManyField(blank=True, related_name='essay_methods', to='internal.SampleType'),
        ),
        migrations.AddField(
            model_name='essayfill',
            name='quotation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='essay_fills', to='internal.Quotation'),
        ),
        migrations.AddField(
            model_name='essayfill',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Sample'),
        ),
        migrations.AddField(
            model_name='essay',
            name='essay_methods',
            field=models.ManyToManyField(blank=True, related_name='essays', to='internal.EssayMethod'),
        ),
        migrations.AddField(
            model_name='basicuser',
            name='roles',
            field=models.ManyToManyField(to='internal.Role'),
        ),
        migrations.AddField(
            model_name='basicuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Client'),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Employee'),
        ),
        migrations.AddField(
            model_name='servicecontract',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Client'),
        ),
        migrations.AddField(
            model_name='laboratory',
            name='employees',
            field=models.ManyToManyField(blank=True, related_name='laboratories', to='internal.Employee'),
        ),
        migrations.AddField(
            model_name='laboratory',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='internal.Employee'),
        ),
        migrations.AddField(
            model_name='employee',
            name='assigned_essay_methods',
            field=models.ManyToManyField(blank=True, related_name='employees', to='internal.EssayMethodFill'),
        ),
        migrations.AddField(
            model_name='employee',
            name='essay_methods',
            field=models.ManyToManyField(blank=True, related_name='employees', to='internal.EssayMethod'),
        ),
    ]
