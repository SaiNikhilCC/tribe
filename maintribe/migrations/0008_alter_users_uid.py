# Generated by Django 4.1.7 on 2023-05-23 06:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("maintribe", "0007_alter_users_uid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="uid",
            field=models.UUIDField(
                default=uuid.UUID("b8a3b942-8a78-47a7-bf9d-5f313b34af2a"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
