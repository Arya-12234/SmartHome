# Generated by Django 5.1.3 on 2024-11-28 08:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpreferences',
            name='notifications_enabled',
        ),
        migrations.RemoveField(
            model_name='userpreferences',
            name='theme',
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='heating_shower',
            field=models.CharField(choices=[('on', 'On'), ('off', 'Off')], default='off', max_length=10),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='lighting_day',
            field=models.CharField(choices=[('dim', 'Dim'), ('bright', 'Bright')], default='bright', max_length=10),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='lighting_night',
            field=models.CharField(choices=[('dim', 'Dim'), ('bright', 'Bright')], default='bright', max_length=10),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='security_alarm',
            field=models.CharField(choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')], default='enabled', max_length=10),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='security_curtains',
            field=models.CharField(choices=[('auto', 'Automatic'), ('manual', 'Manual')], default='auto', max_length=10),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='security_gate',
            field=models.CharField(choices=[('auto', 'Automatic'), ('manual', 'Manual')], default='auto', max_length=10),
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
