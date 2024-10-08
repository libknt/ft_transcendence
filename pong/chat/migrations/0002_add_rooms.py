# Generated by Django 5.0.3 on 2024-07-27 09:16

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_add_room_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rooms",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=20, unique=True)),
                ("password", models.CharField(blank=True, max_length=20, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "room_status_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="chat.roomstatus",
                    ),
                ),
            ],
            options={
                "verbose_name": "room",
                "verbose_name_plural": "rooms",
                "db_table": "rooms",
                "ordering": ["-created_at"],
            },
        ),
    ]
