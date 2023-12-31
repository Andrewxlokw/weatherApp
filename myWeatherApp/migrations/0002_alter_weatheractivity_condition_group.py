# Generated by Django 4.2.5 on 2023-11-05 02:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myWeatherApp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="weatheractivity",
            name="condition_group",
            field=models.CharField(
                choices=[
                    ("severe", "Severe"),
                    ("default", "Default"),
                    ("2xx", "Thunderstorm"),
                    ("3xx", "Drizzle"),
                    ("5xx", "Rain"),
                    ("6xx", "Snow"),
                    ("7xx", "Atmosphere"),
                    ("800", "Clear"),
                    ("80x", "Clouds"),
                ],
                default="default",
                max_length=10,
            ),
        ),
    ]
