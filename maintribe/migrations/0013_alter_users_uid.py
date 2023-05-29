# Generated by Django 4.1.7 on 2023-05-23 06:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("maintribe", "0012_alter_users_uid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="uid",
            field=models.UUIDField(
                default=uuid.UUID("a8210685-7a94-4031-8ae6-ff4e63ce8621"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]