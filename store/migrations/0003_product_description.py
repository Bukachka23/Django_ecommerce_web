# Generated by Django 4.2.2 on 2023-06-28 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_product_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
