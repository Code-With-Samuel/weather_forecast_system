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

            # 🔥 Request JWT token from FastAPI
            login_url = "http://127.0.0.1:8000/auth/login"  # Make sure FastAPI is running on port 8000

            response = requests.post(login_url, data={"username": user.username, "password": request.POST.get("password")}, headers={"Content-Type": "application/x-www-form-urlencoded"})

            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("access_token")

                if access_token:
                    # ✅ Store token in Django session
                    request.session["access_token"] = access_token
                    print(f"✅ Stored token: {access_token}")  # Debugging

            else:
                print(f"FASTAPI Login Failed: {response.status_code}, {response.text}")

            return redirect('dashboard:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        # 🔥 Clear session token on logout
        request.session.pop("access_token", None)
        logout(request)
        return redirect('accounts:login')

@login_required
def dashboard_view(request):
    city = "Kathmandu"  # Default city

    # 🔥 Retrieve token from session
    access_token = request.session.get("access_token")
    print(f"Stored token: {access_token}")  # Debugging

    headers = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    # Fetch current weather data
    weather_data = None
    try:
        response = requests.get(f'http://127.0.0.1:8000/weather/current_weather?city={city}', headers=headers)
        if response.status_code == 200:
            weather_data = response.json()
        else:
            print(f"❌ Weather API Response: {response.status_code}, {response.text}")  # Debugging
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching weather data: {e}")

    # Fetch 3-day forecast data
    forecast_data = None
    try:
        forecast_response = requests.get(f'http://127.0.0.1:8000/weather/forecast?city={city}', headers=headers)
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
        else:
            print(f"❌ Forecast API Response: {forecast_response.status_code}, {forecast_response.text}")  # Debugging
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching forecast data: {e}")

    return render(request, 'dashboard/home.html', {
        'weather_data': weather_data,
        'forecast_data': forecast_data
    })
