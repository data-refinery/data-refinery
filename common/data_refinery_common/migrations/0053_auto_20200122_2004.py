# Generated by Django 2.2.9 on 2020-01-22 20:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_refinery_common", "0052_remove_invalid_tximport_associations"),
    ]

    operations = [
        migrations.AddField(
            model_name="compendiumresult",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name="compendiumresult",
            name="last_modified",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
