# Generated by Django 5.0.1 on 2024-03-01 10:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0023_alter_cartitem_size"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="size",
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
