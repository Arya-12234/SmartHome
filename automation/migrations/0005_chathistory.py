# Generated by Django 5.0.7 on 2024-12-02 10:48

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0004_alter_device_total_usage_time'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('message_type', models.CharField(choices=[('user', 'User'), ('system', 'System'), ('error', 'Error')], default='user', max_length=10)),
                ('user_message', models.TextField()),
                ('bot_response', models.TextField()),
                ('device', models.CharField(blank=True, max_length=100, null=True)),
                ('command', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('success', 'Success'), ('failure', 'Failure'), ('pending', 'Pending')], default='pending', max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]