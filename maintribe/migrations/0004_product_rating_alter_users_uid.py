# Generated by Django 4.1.7 on 2023-05-23 06:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("maintribe", "0003_alter_ordermodel_order_confirmedat_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="rating",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="users",
            name="uid",
            field=models.UUIDField(
                default=uuid.UUID("b0980de3-77c7-4129-aa56-4a6b507efd91"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]