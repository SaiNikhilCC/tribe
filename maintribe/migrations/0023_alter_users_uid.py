# Generated by Django 4.1.7 on 2023-05-23 10:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("maintribe", "0022_alter_reviews_description_alter_reviews_subject_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="uid",
            field=models.UUIDField(
                default=uuid.UUID("2ed274a0-a9d2-48b7-9480-57f06e7ff66b"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]