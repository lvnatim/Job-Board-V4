# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-16 00:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0007_auto_20160412_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='due_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
