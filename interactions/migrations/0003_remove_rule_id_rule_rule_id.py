# Generated by Django 5.0.3 on 2024-03-23 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0002_alter_rule_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rule',
            name='id',
        ),
        migrations.AddField(
            model_name='rule',
            name='rule_id',
            field=models.AutoField(default=None, primary_key=True, serialize=False),
        ),
    ]
