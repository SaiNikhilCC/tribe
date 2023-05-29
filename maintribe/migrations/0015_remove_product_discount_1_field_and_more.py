# Generated by Django 4.1.7 on 2023-05-23 06:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        (
            "maintribe",
            "0014_product_discount_1_field_product_discount_2_field_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="discount_1_field",
        ),
        migrations.RemoveField(
            model_name="product",
            name="discount_2_field",
        ),
        migrations.RemoveField(
            model_name="product",
            name="discount_3_field",
        ),
        migrations.RemoveField(
            model_name="product",
            name="discount_4_field",
        ),
        migrations.RemoveField(
            model_name="product",
            name="discount_5_field",
        ),
        migrations.AlterField(
            model_name="users",
            name="uid",
            field=models.UUIDField(
                default=uuid.UUID("3b517e5a-c13d-4ac2-85b3-56df9fd578e1"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
