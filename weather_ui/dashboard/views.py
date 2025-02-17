from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests

@login_required(login_url="accounts:login")
def home(request):
    weather_data = None
    forecast_data = None
    city = "Kathmandu"  # Default city (you can change this)

    if request.method == 'POST':
        city = request.POST.get('city')  # Get city from form input

    #Get user token from Django session (assuming you store it at login)
    token = request.session.get("access_token")

    print(f"Stored token: {token}") #Debugging

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    if city:
        # Replace with your actual FastAPI endpoints
        weather_api_url = f'http://127.0.0.1:8080/weather/current_weather?city={city}'
        forecast_api_url = f'http://127.0.0.1:8080/weather/forecast?city={city}'

        # Fetch real-time weather data
        weather_response = requests.get(weather_api_url)
        print("Weather API Response:", weather_response.text)  # Debugging
        if weather_response.status_code == 200:
            weather_data = weather_response.json()

        # Fetch 3-day weather forecast
        forecast_response = requests.get(forecast_api_url)
        print("Forecast API Response:", forecast_response.text)  # Debugging
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()

    return render(request, 'dashboard/home.html', {
        'weather_data': weather_data,
        'forecast_data': forecast_data,
        'selected_city': city
    })