# Generated by Django 5.0.3 on 2024-03-16 12:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentRequest',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Request_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('transaction_ref', models.CharField(max_length=100)),
                ('request_note', models.TextField(blank=True, null=True)),
                ('payment_note', models.CharField(blank=True, max_length=250, null=True)),
                ('Transaction_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=200)),
                ('Initiator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_initiator', to=settings.AUTH_USER_MODEL)),
                ('Payer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_payer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]