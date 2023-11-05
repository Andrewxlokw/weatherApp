from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse, HttpResponse

from .models import WeatherActivity

from utils import SEVERE_WEATHER_CODES

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
import json
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, "index.html")


def weather(request):
    api_key = "21ce77d1d073431c87f181124232710"
    base_url = "http://api.weatherapi.com/v1/current.json"
    
    # Hardcoded for testing purposes
    city = "London"  
    unit = "c"  # 'c' for Celsius, 'f' for Fahrenheit
    weather_data={}
    if request.method == 'POST':
        city = request.POST.get('city', city)
        unit = request.POST.get('unit', unit)

    final_url = f"{base_url}?key={api_key}&q={city}"


    try:
        response = requests.get(final_url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()

        temperature = data["current"]["temp_c"] if unit == 'c' else data["current"]["temp_f"]

        weather_data = {
            "city": city,
            "temperature": temperature,
            "condition": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"],
            "unit": unit,
        }
    except requests.exceptions.HTTPError as e:
        # If the city is not found or any other HTTP error occurred, inform the user.
        messages.error(request, "Failed to retrieve weather data. Please try a different city.")

    return render(request, "weather.html", weather_data)


# def get_user_city(request):
#     ip_address = request.META.get("REMOTE_ADDR", None)
#     if ip_address:
#         city = get_city_from_ip(ip_address)
#         return JsonResponse({"city": city})
#     return JsonResponse({"city": "Unknown"})


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