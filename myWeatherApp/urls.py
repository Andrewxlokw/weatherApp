from django.urls import path, include
from . import views
# from .views import SignUpView, weather_api, LoginView
from .views import  weather_api, my_login, get_default_city, set_default_city, api_logout, check_login_status, api_sign_up
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('api/signup/', api_sign_up, name='signup_api'),
    path('api/login/', my_login, name='login_api'),
    path('api/logout/', api_logout, name='logout_api'),

    path('api/weather-data', weather_api, name='weather_api'),
    path('api/get-default-city/', get_default_city, name='get_default_city'),
    path('api/set-default-city/', set_default_city, name='set_default_city'),
    path('api/check-login-status/', check_login_status, name='check-login-status'),
]
