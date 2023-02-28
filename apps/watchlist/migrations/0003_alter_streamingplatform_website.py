# Generated by Django 4.1.5 on 2023-02-27 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("watchlist", "0002_alter_movie_platform"),
    ]

    operations = [
        migrations.AlterField(
            model_name="streamingplatform",
            name="website",
            field=models.URLField(
                blank=True, default="", max_length=100, verbose_name="Website URL"
            ),
        ),
    ]