# Generated by Django 5.0.3 on 2024-04-01 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bayesian', '0002_rename_drug_drug_bayesian'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='drug_bayesian',
            table='Drugs_bayesian',
        ),
    ]
