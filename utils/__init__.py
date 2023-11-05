import requests


def get_city_from_ip(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        data = response.json()
        return data.get("city", "try: Unknown City" + ip_address)
    except Exception as e:
        print(f"Error getting city from IP: {e}")
        return "exception: Unknown City"


SEVERE_WEATHER_CODES = {
    200, 201, 202,  # Thunderstorm
    210, 211, 212, 221,  # Thunderstorm
    230, 231, 232,  # Thunderstorm
    502, 503, 504,  # Rain
    511,  # Freezing rain
    520, 521, 522, 531,  # Rain
    602,  # Heavy snow
    611, 612, 613,  # Sleet
    615, 616,  # Rain and snow
    620, 621, 622,  # Snow showers
    711,  # Smoke
    731,  # Sand/dust whirls
    751, 761,  # Sand, dust
    762,  # Volcanic ash
    771,  # Squalls
    781,  # Tornado
}

# You can now use this set to check if a given weather code is considered 'severe'.
