# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-03-23 16:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_auto_20190323_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='user',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room', to=settings.AUTH_USER_MODEL),
        ),
    ]