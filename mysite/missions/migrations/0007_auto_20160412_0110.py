# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-12 01:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0006_auto_20160412_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='priority',
            name='color',
            field=models.CharField(max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='priority_mission',
            name='color',
            field=models.CharField(max_length=7, null=True),
        ),
    ]