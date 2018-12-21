# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-08-31 01:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bicycleparking', '0010_betacomments'),
    ]

    operations = [
        migrations.AddField(
            model_name='approval',
            name='status',
            field=models.TextField(default='OK'),
        ),
        migrations.AlterField(
            model_name='approval',
            name='moderatorId',
            field=models.TextField(default='', null=True),
        ),
    ]