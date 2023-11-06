# Standard library imports
import json
import logging

# Django imports
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

# Third-party imports
import requests

# Local application imports
from .models import UserPreference, WeatherGroup
from utils import SEVERE_WEATHER_CODES

# for debugging only
logger = logging.getLogger(__name__)


def index(request):
    return render(request, "index.html")


def get_activity_recommendation(request: HttpRequest, weather_code:int) -> JsonResponse:
    """
    Gets activity recommendation based on the weather code.
    """
    # change the weather_code from int to a string
    weather_code = str(weather_code)

    # Get the condition group
    if weather_code in SEVERE_WEATHER_CODES:
        condition_group = 'severe'
    elif weather_code == 'default':
        condition_group = 'default'
    # Check if the weather_code is '800' for clear skies
    elif weather_code == '800':
        condition_group = '800'
    elif 801 <= int(weather_code) <= 809:
        condition_group = '80x'
    else:
        condition_group = weather_code[0] + 'xx'
    
    # Try to get the activity recommendation from the WeatherGroup based on the condition_group
    try:
        recommendation = WeatherGroup.objects.get(condition_group=condition_group)
        activity = recommendation.activity_recommendation
    except WeatherGroup.DoesNotExist:
        activity = "No recommendation for this weather."
    
    return {
        'activity_recommendation': activity,
    }


def weather(request: HttpRequest) -> HttpResponse:
    """
        Handle requests to the weather page and retrieve weather information for the user's preferred or default city.
    """
    # api key for openweathermap.org
    # link https://home.openweathermap.org/api_keys
    api_key = "5c7a73ace0d65e545d96bc25182d0289"

    # chatgpt wrote this comment, im so bad at discribing it 
    # If the user is logged in, retrieve their preferred city from the UserPreference model, defaulting to "Shanghai" if no preferred city is set. 
    # If the user is not logged in, default the city to "Beijing".
    if request.user.is_authenticated:
        user_profile, created = UserPreference.objects.get_or_create(user=request.user)
        city_name = user_profile.preferred_city or "Shanghai"
    else:
        city_name = "Beijing"

    # default values
    unit = "metric"  # 'metric' for Celsius, 'imperial' for Fahrenheit
    weather_info={}

    # when user updates the city name, try to display the city's weather information
    if request.method == 'POST':
        city_name = request.POST.get('city',city_name)
        unit = request.POST.get('unit',unit)

    # Get latitude and longitude of the city name
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    try:
        geo_response = requests.get(geocoding_url)

        # check for http related error, part 1, source: chatgpt
        geo_response.raise_for_status()  


        geo_data = geo_response.json()

        if geo_data:
            # Get latitude and longitude using city name
            # documentation: https://openweathermap.org/api/geocoding-api
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']

            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={unit}&appid={api_key}"
            
            weather_response = requests.get(weather_url)

            # source: chatgpt
            weather_response.raise_for_status()


            weather_data = weather_response.json()
            # get the weather condition ID from the weather data, and get the activity recommendation
            weather_condition_ID = weather_data['weather'][0]['id']
            activity_recommendation = get_activity_recommendation(request, weather_condition_ID)

            # documentation: https://openweathermap.org/current
            weather_info = {
                "city": city_name.title(),
                "temperature": weather_data["main"]["temp"],
                "condition": weather_data["weather"][0]["description"],
                "icon": weather_data["weather"][0]["icon"],
                "humidity": weather_data["main"]["humidity"],
                "wind_speed": weather_data["wind"]["speed"],
                "activity": activity_recommendation['activity_recommendation']
            }
        else:
            # If the city is not found, return error.
            weather_info = {"error": "Error: City name not found."}
    # part 2, source: chatgpt
    except requests.exceptions.HTTPError as e:
            # If the city is not found or any other HTTP error occurred, inform the user.
            messages.error(request, "Error: Failed to retrieve weather data from the api.")

    return render(request, "weather.html", {'weather_info': weather_info, 'unit': unit})


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') 
    template_name = 'signup.html'
    
    def form_valid(self, form) -> HttpResponse:
        """
        Process the valid form, log the user in, and redirect to the success URL (login).
        """
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)



@login_required
def set_default_city(request: HttpRequest) -> HttpResponseRedirect:
    """
        Sets the default city for the logged-in user based on their selection.
    """
    if request.method == 'POST':
        preferred_city = request.POST.get('default_city')
        
        #source: https://stackoverflow.com/questions/1941212/how-to-use-get-or-create-in-django
        user_preference, created = UserPreference.objects.get_or_create(user=request.user)

        user_preference.preferred_city = preferred_city
        user_preference.save()
    return redirect('weather')  