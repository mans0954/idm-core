# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-11 21:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('name', '0005_namecontext_subject_to_acceptance'),
    ]

    operations = [
        migrations.RunSQL(
            "DROP INDEX name_any_unique",
            "CREATE UNIQUE INDEX name_any_unique ON name_name (identity_id, context_id) WHERE context_id IN ('presentational', 'legal', 'card')",
        ),
        migrations.RunSQL(
            "CREATE UNIQUE INDEX name_any_unique ON name_name (identity_id, state, context_id) WHERE context_id IN ('presentational', 'legal', 'card') AND state IN ('proposed', 'accepted')",
            "DROP INDEX name_any_unique",
        ),
    ]
