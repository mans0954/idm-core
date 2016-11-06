# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 15:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('person', '0001_initial'),
        ('attestation', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcedocument',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_documents', to='person.Person'),
        ),
        migrations.AddField(
            model_name='sourcedocument',
            name='validated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='validated_source_documents', to='person.Person'),
        ),
        migrations.AddField(
            model_name='attestation',
            name='source_document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attestation.SourceDocument'),
        ),
        migrations.AddField(
            model_name='attestation',
            name='supports_content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
