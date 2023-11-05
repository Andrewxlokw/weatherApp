from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse, HttpResponse

from .models import WeatherActivity, UserPreference

from utils import SEVERE_WEATHER_CODES

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
import json
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, "index.html")


def weather(request):
    # api_key = "21ce77d1d073431c87f181124232710"
    # base_url = "http://api.weatherapi.com/v1/current.json"

    api_key = "5c7a73ace0d65e545d96bc25182d0289"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    print("running weather")
    # Hardcoded for testing purposes
    if request.user.is_authenticated:
        user_profile, created = UserPreference.objects.get_or_create(user=request.user)
        city_name = user_profile.preferred_city or "Shanghai"
    else:
        city_name = "Beijing"
    # city_name = "London"  

    unit = "metric"  # 'c' for Celsius, 'f' for Fahrenheit
    weather_info={}
    if request.method == 'POST':
        city_name = request.POST.get('city',city_name)
        unit = request.POST.get('unit',unit)


        # final_url = f"{base_url}?key={api_key}&q={city}"

        # Step 1: Get latitude and longitude from city name
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    try:
        geo_response = requests.get(geocoding_url)
        geo_response.raise_for_status()  # This will check for HTTP errors
        geo_data = geo_response.json()

        if geo_data:
            # Step 2: Get weather information using the latitude and longitude
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
            print("lat",lat)
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={unit}&appid={api_key}"
            
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            weather_info = {
                "city": city_name.title(),
                "temperature": weather_data["main"]["temp"],
                "condition": weather_data["weather"][0]["description"],
                "icon": weather_data["weather"][0]["icon"],
                "condition_id": weather_data["weather"][0]["id"],
                "humidity": weather_data["main"]["humidity"]
            }
        else:
            weather_info = {"error": "City not found."}
    except requests.exceptions.HTTPError as e:
            # If the city is not found or any other HTTP error occurred, inform the user.
            messages.error(request, "Failed to retrieve weather data. Please try a different city.")

    return render(request, "weather.html", {'weather_info': weather_info, 'unit': unit})



def location(request):
    response_string = "The IP address {} is located at the coordinates {}, which is in the city {}.".format(
        request.ipinfo.ip, request.ipinfo.loc, request.ipinfo.city
    )

    return HttpResponse(response_string)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    # success_url = reverse_lazy('login')  # or 'index' if you want to redirect to the home page
    success_url = reverse_lazy('index') 
    template_name = 'signup.html'
    
    def form_valid(self, form):
        # Save the new user first
        user = form.save()
        # Then log the user in
        login(self.request, user)
        # Finally redirect to the target page
        return super().form_valid(form)


#return re
def get_activity_recommendation(request, weather_code):

    # Convert weather_code to integer if it's not already, since the codes in the set are integers. not necessary!!!!!!!!!
    weather_code = int(weather_code)

    if weather_code in SEVERE_WEATHER_CODES:
        condition_group = 'severe'
    # Check if the weather_code is '800' for clear skies
    elif weather_code == '800':
        condition_group = '800'
    else:
        # For all other codes, use the first digit and 'xx' as a placeholder
        condition_group = weather_code[:1] + 'xx'
    
    # Try to get the activity recommendation based on the condition group
    try:
        recommendation = WeatherActivity.objects.get(condition_group=condition_group)
        activity = recommendation.activity_recommendation
    except WeatherActivity.DoesNotExist:
        activity = "No specific recommendation for this weather."
    
    # Construct a dictionary to serialize to JSON
    response_data = {
        #not needed
        'condition_code': weather_code,
        #needed
        'activity_recommendation': activity,
    }
    
    # Serialize the data and create an HttpResponse object
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

@login_required
def set_preferred_city(request):
    if request.method == 'POST':
        preferred_city = request.POST.get('preferred_city')
        user_profile, created = UserPreference.objects.get_or_create(user=request.user)
        user_profile.preferred_city = preferred_city
        user_profile.save()
        messages.success(request, "Preferred city updated.")
    return redirect('weather')  # Replace with the name of your profile page's URL