# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-09-29 09:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20190929_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='post.Post'),
        ),
    ]
