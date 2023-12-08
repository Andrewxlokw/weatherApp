from django.urls import path, include
from . import views
# from .views import SignUpView, weather_api, LoginView
from .views import SignUpView, weather_api, my_login, get_default_city, set_default_city, api_logout, check_login_status,get_activity_recommendation
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('weather/', views.weather, name='weather'),  # <-- Add this
    path("signup/", SignUpView.as_view(), name="signup"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('get_activity_recommendation/<str:weather_code>/', views.get_activity_recommendation, name='get_activity_recommendation'),
    # path('set_default_city/', views.set_default_city, name='set_default_city'),
    path('api/weather-data', weather_api, name='weather_api'),

    # path('api/signup/', views.signup_view, name='signup'),

    # path('api/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('api/signup/', SignUpView.as_view(), name="signup"),
    path('api/login/', my_login, name='login_api'),
    path('api/logout/', api_logout, name='logout_api'),

    path('api/get-default-city/', get_default_city, name='get_default_city'),
    path('api/set-default-city/', set_default_city, name='set_default_city'),
    path('api/check-login-status/', check_login_status, name='check-login-status'),

    #  path('api/activity-recommendation/<int:weather_code>/', get_activity_recommendation, name='activity-recommendation'),

]
