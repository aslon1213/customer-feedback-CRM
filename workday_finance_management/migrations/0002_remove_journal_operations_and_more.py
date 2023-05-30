# Generated by Django 4.2 on 2023-05-28 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workday_finance_management", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="journal",
            name="operations",
        ),
        migrations.AlterField(
            model_name="operation",
            name="operation_type",
            field=models.CharField(
                choices=[("TRANSFER", "TRANSFER"), ("CASH", "CASH"), ("CARD", "CARD")],
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name="journal",
            name="operations",
            field=models.ManyToManyField(
                related_name="journal", to="workday_finance_management.operation"
            ),
        ),
    ]
