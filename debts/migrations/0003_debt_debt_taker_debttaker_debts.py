# Generated by Django 4.2 on 2023-05-09 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("debts", "0002_debttaker"),
    ]

    operations = [
        migrations.AddField(
            model_name="debt",
            name="debt_taker",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="debt_taker",
                to="debts.debttaker",
            ),
        ),
        migrations.AddField(
            model_name="debttaker",
            name="debts",
            field=models.ManyToManyField(
                blank=True, related_name="debt", to="debts.debt"
            ),
        ),
    ]
