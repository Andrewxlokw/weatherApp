from django.urls import path, include
from . import views
from .views import SignUpView, weather_api
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('weather/', views.weather, name='weather'),  # <-- Add this
    path("signup/", SignUpView.as_view(), name="signup"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('get_activity_recommendation/<str:weather_code>/', views.get_activity_recommendation, name='get_activity_recommendation'),
    path('set_default_city/', views.set_default_city, name='set_default_city'),
    path('api/weather-data', weather_api, name='weather_api'),

]
