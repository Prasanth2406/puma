# Generated by Django 5.0.1 on 2024-02-20 04:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0009_rename_image_gymandaccessories_simage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gymandaccessories",
            name="simage",
            field=models.ImageField(upload_to="gym_images/"),
        ),
    ]