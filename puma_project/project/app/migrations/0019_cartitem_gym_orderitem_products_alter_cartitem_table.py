# Generated by Django 5.0.1 on 2024-02-29 08:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0018_remove_cartitem_gym_remove_orderitem_products_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="gym",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app.gymandaccessories",
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="products",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.gymandaccessories",
            ),
        ),
        migrations.AlterModelTable(
            name="cartitem",
            table="cart_items_gym",
        ),
    ]
