# Generated by Django 4.2 on 2023-05-29 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "workday_finance_management",
            "0003_operation_journal_alter_journal_operations_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="journal",
            name="date",
            field=models.DateField(unique=True),
        ),
        migrations.AlterField(
            model_name="operation",
            name="operation_type",
            field=models.CharField(
                choices=[("TRANSFER", "TRANSFER"), ("CARD", "CARD"), ("CASH", "CASH")],
                max_length=100,
            ),
        ),
    ]
