# Generated by Django 5.0.1 on 2024-03-01 08:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0021_winter_cartitem_winter_orderitem_productss"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="size",
            field=models.CharField(default=0, max_length=50),
        ),
    ]
