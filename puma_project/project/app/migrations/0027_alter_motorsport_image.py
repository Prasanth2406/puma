# Generated by Django 5.0.1 on 2024-03-02 06:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0026_motorsport_cartitem_ms_orderitem_prods"),
    ]

    operations = [
        migrations.AlterField(
            model_name="motorsport",
            name="image",
            field=models.ImageField(upload_to="motor_images"),
        ),
    ]
