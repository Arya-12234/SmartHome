# Generated by Django 5.0.7 on 2024-12-04 09:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0009_feature'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterModelOptions(
            name='chathistory',
            options={'verbose_name_plural': 'Chat Histories'},
        ),
        migrations.AddField(
            model_name='chathistory',
            name='error_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chathistory',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automation.device'),
        ),
        migrations.AlterField(
            model_name='chathistory',
            name='status',
            field=models.CharField(choices=[('success', 'Success'), ('failure', 'Failure'), ('pending', 'Pending'), ('executed', 'Executed'), ('not_supported', 'Not Supported'), ('validation_failed', 'Validation Failed')], default='pending', max_length=20),
        ),
        migrations.AddIndex(
            model_name='chathistory',
            index=models.Index(fields=['timestamp'], name='automation__timesta_a96cd2_idx'),
        ),
        migrations.AddField(
            model_name='payment',
            name='pricing_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='automation.pricingplan'),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
