# Generated by Django 5.0.1 on 2024-03-03 05:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0027_alter_motorsport_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone", models.IntegerField()),
            ],
        ),
    ]
