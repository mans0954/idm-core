# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 17:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('name', '0001_initial'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='name',
            name='identity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='names', to='person.Person'),
        ),
    ]
