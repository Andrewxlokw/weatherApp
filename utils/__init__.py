import requests


# update 2023/11 https://openweathermap.org/weather-conditions
SEVERE_WEATHER_CODES = {
    # Thunderstorm
    200, 201, 202,  
    210, 211, 212, 
    221,  
    230, 231, 232, 
    # Rain 
    502, 503, 504,  
    511, 520, 521, 522, 
    531,  
    # Heavy snow and Sleet
    602,  
    611, 612, 613,  
    615, 616,
    620, 621, 622,
    # Rare weather
    711,  # Smoke
    731,  # Dust whirls
    751,  # Sand
    761,  # dust
    762,  # Volcanic ash
    771,  # Squalls
    781,  # Tornado
}

