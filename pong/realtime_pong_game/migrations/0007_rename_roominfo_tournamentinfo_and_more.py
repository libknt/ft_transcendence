# Generated by Django 5.0.3 on 2024-09-01 03:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("realtime_pong_game", "0006_remove_matchinfo_winner"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="RoomInfo",
            new_name="TournamentInfo",
        ),
        migrations.RenameField(
            model_name="matchinfo",
            old_name="room_info",
            new_name="tournament_info",
        ),
        migrations.RenameField(
            model_name="tournamentinfo",
            old_name="room_name",
            new_name="tournament_name",
        ),
        migrations.DeleteModel(
            name="RoomParticipantMapper",
        ),
    ]
