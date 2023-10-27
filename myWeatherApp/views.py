from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    return render(request, 'index.html')

def weather(request):
    api_key = "21ce77d1d073431c87f181124232710"
    base_url = "http://api.weatherapi.com/v1/current.json"

    city = "Ottawa"  # Hardcoded for this example, you can make it dynamic

    final_url = f"{base_url}?key={api_key}&q={city}"


    response = requests.get(final_url)
    data = response.json()

    weather_data = {
        'city': city,
        'temperature': data['current']['temp_c'],
        'condition': data['current']['condition']['text'],
        'icon': data['current']['condition']['icon'],
    }

    return render(request, 'weather.html', weather_data)