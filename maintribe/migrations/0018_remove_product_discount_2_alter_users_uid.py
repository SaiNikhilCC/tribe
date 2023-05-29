# Generated by Django 4.1.7 on 2023-05-23 06:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("maintribe", "0017_product_discount_2_alter_users_uid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="discount_2",
        ),
        migrations.AlterField(
            model_name="users",
            name="uid",
            field=models.UUIDField(
                default=uuid.UUID("c4dd9bb5-ce5a-41c0-9b5a-d142f82c958f"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]