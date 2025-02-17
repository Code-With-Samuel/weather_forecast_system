import requests
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard:home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')


# Dashboard view - we added the login_required decorator here
@login_required
def dashboard_view(request):
    city = "Kathmandu"  # You can change this to dynamic city input from the user

    # Fetch current weather data
    weather_data = None
    try:
        response = requests.get(f'http://127.0.0.1:8000/current_weather?city={city}', 
                                headers={'Authorization': f'Bearer {request.user.auth_token}'})
        if response.status_code == 200:
            weather_data = response.json()  # Weather data from FastAPI
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")

    # Fetch 3-day forecast data
    forecast_data = None
    try:
        forecast_response = requests.get(f'http://127.0.0.1:8000/forecast?city={city}',
                                         headers={'Authorization': f'Bearer {request.user.auth_token}'})
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()  # Forecast data from FastAPI
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast data: {e}")

    return render(request, 'dashboard/home.html', {'weather_data': weather_data, 'forecast_data': forecast_data})
