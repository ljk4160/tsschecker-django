# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-07-10 05:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('ecid', models.CharField(editable=False, max_length=16, primary_key=True, serialize=False, unique=True, verbose_name='ECID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('hw_model', models.CharField(help_text='Example: n90ap', max_length=16, verbose_name='HW Model')),
                ('product_type', models.CharField(help_text='Example: iPhone10,3', max_length=16, verbose_name='Product Type')),
                ('ios_version', models.CharField(help_text='Example: 11.4', max_length=16, verbose_name='iOS Version')),
                ('ios_build', models.CharField(blank=True, default='', help_text='Example: 15F5061e', max_length=16, verbose_name='iOS Build')),
                ('generator', models.CharField(blank=True, max_length=32, verbose_name='Generator')),
            ],
            options={
                'verbose_name': 'Meta',
                'verbose_name_plural': 'Metas',
            },
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('blob_version', models.CharField(help_text='Example: 11.4', max_length=16, verbose_name='Blob Version')),
                ('blob_build', models.CharField(help_text='Example: 15F5061e', max_length=16, verbose_name='Blob Build')),
                ('ap_nonce', models.CharField(blank=True, max_length=64, verbose_name='Blob Nonce')),
                ('blob_file', models.FileField(blank=True, help_text='Choose a Blob File (*.shsh2) to upload', max_length=255, null=True, upload_to='shsh2', verbose_name='Blob File')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MetaManagement.Device', verbose_name='Device')),
            ],
            options={
                'verbose_name': 'Signature',
                'verbose_name_plural': 'Signatures',
            },
        ),
    ]