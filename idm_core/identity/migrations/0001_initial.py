# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 17:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import idm_core.identity.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('uuid', models.UUIDField(default=idm_core.identity.models.get_uuid, editable=False, primary_key=True, serialize=False)),
                ('identity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='identity.Identity')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
