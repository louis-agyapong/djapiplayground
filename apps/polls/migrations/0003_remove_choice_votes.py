# Generated by Django 4.1.5 on 2023-01-15 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0002_remove_vote_votes_choice_votes_alter_choice_poll"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="choice",
            name="votes",
        ),
    ]