# Generated by Django 4.2 on 2023-05-09 18:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("debts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DebtTaker",
            fields=[
                ("first_name", models.CharField(max_length=120)),
                ("last_name", models.CharField(blank=True, max_length=120, null=True)),
                ("telephone", models.CharField(blank=True, max_length=120, null=True)),
                ("email", models.EmailField(blank=True, max_length=120, null=True)),
                (
                    "telegram_username",
                    models.CharField(blank=True, max_length=120, null=True),
                ),
                (
                    "passport_series",
                    models.CharField(blank=True, max_length=120, null=True),
                ),
                (
                    "ID",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
            ],
        ),
    ]
