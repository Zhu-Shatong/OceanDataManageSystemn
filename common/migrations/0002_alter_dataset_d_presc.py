# Generated by Django 4.2.13 on 2024-06-15 12:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dataset",
            name="d_presc",
            field=models.CharField(max_length=500),
        ),
    ]