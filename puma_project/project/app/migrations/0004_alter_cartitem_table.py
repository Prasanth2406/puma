# Generated by Django 5.0.1 on 2024-02-07 13:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_customer_cartitem"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="cartitem",
            table="cart_items",
        ),
    ]
