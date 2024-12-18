# Generated by Django 5.1.3 on 2024-11-28 13:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from datetime import timedelta

class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0002_remove_userpreferences_notifications_enabled_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='last_used',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='total_usage_time',
            field=models.DurationField(default=timedelta()),
        ),
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
