from django.db import models

# Create your models here.


class WeatherActivity(models.Model):
    WEATHER_CONDITION_GROUP_CODE  = [
        # not part of the weather code from openweathermap.org
        ('severe', 'Severe'),
        ('default', 'Default'),
        # weather code updated 2023-11-01 https://openweathermap.org/weather-conditions
        ('2xx', 'Thunderstorm'),
        ('3xx', 'Drizzle'),
        ('5xx', 'Rain'),
        ('6xx', 'Snow'),
        ('7xx', 'Atmosphere'),
        ('800', 'Clear'),
        ('80x', 'Clouds'),
        
    ]


    condition_group = models.CharField(
        max_length=10,
        choices=WEATHER_CONDITION_GROUP_CODE,
        # unique=True,
        default='default',
    )
    activity_recommendation = models.TextField()

    def __str__(self):
        return self.get_condition_group_display()
        # # Return a string representation of the model.
        # group_display = dict(WEATHER_CONDITION_GROUP_CODE).get(self.condition_group, "Unknown")
        # return f"{group_display} - {self.activity_recommendation}"