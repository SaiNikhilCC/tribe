# Generated by Django 4.1.7 on 2023-05-23 10:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("maintribe", "0021_alter_users_uid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviews",
            name="description",
            field=models.TextField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="reviews",
            name="subject",
            field=models.CharField(blank=True, default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="users",
            name="uid",
            field=models.UUIDField(
                default=uuid.UUID("fea94308-7d02-4360-b16a-6dfd9137c79b"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
