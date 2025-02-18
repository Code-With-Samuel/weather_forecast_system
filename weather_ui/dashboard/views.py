from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages

FASTAPI_BASE_URL = "http://127.0.0.1:8080"

@login_required(login_url="accounts:login")
def home(request):
    weather_data = None
    forecast_data = None
    city = "Kathmandu"  # Default city

    if request.method == 'POST':
        city = request.POST.get('city', city)  # Get city from form input

    # Get user token from Django session
    token = request.session.get("access_token")

    # print(f"Stored token: {token}")  # Debugging

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    else:
        messages.error(request, "Authentication required. Please log in.")
        return redirect("accounts:login")

    if city:
        # Replace with your actual FastAPI endpoints
        weather_api_url = f'{FASTAPI_BASE_URL}/weather/current_weather?city={city}'
        forecast_api_url = f'{FASTAPI_BASE_URL}/weather/forecast?city={city}'

        try:
            # Fetch real-time weather data with token
            weather_response = requests.get(weather_api_url, headers=headers)
            # print("Weather API Response:", weather_response.text)  # Debugging

            if weather_response.status_code == 200:
                weather_data = weather_response.json()
            else:
                messages.error(request, "Failed to fetch current weather data.")

        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error fetching weather data: {e}")

        try:
            # Fetch 3-day weather forecast with token
            forecast_response = requests.get(forecast_api_url, headers=headers)
            # print("Forecast API Response:", forecast_response.text)  # Debugging

            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
            else:
                messages.error(request, "Failed to fetch forecast data.")

        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error fetching forecast data: {e}")

    return render(request, 'dashboard/home.html', {
        'weather_data': weather_data,
        'forecast_data': forecast_data,
        'selected_city': city
    })
