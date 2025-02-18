import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

FASTAPI_BASE_URL = "http://127.0.0.1:8080"

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # 🔥 Send signup data to FastAPI (Optional, if needed)
            signup_url = f"{FASTAPI_BASE_URL}/auth/signup"
            requests.post(signup_url, json={"username": user.username, "password": request.POST['password1']})

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

            login_url = f"{FASTAPI_BASE_URL}/auth/login"
            username = request.POST.get("username")
            password = request.POST.get("password")

            try:
                response = requests.post(
                    login_url, 
                    data={"username": username, "password": password}, 
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )

                if response.status_code == 200:
                    token_data = response.json()
                    access_token = token_data.get("access_token")

                    if access_token:
                        request.session["access_token"] = access_token
                        request.session.modified = True  # ✅ Ensure session updates
                        # print(f"🔑 Token stored: {access_token}")  # Debugging line
                    else:
                        messages.error(request, "Login failed: No access token received.")
                        return redirect('accounts:login')
                else:
                    messages.error(request, "Login failed: Invalid credentials.")
                    return redirect('accounts:login')
            except requests.exceptions.RequestException as e:
                messages.error(request, f"FastAPI connection error: {e}")
                return redirect('accounts:login')

            return redirect('dashboard:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        request.session.pop("access_token", None)
        request.session.modified = True  # ✅ Ensure session updates
        logout(request)
        return redirect('accounts:login')

@login_required
def dashboard_view(request):
    city = "Kathmandu"
    access_token = request.session.get("access_token")

    if not access_token:
        messages.error(request, "You are not authenticated. Please log in.")
        return redirect('accounts:login')

    headers = {"Authorization": f"Bearer {access_token}"}
    weather_data, forecast_data = None, None

    # print(f"✅ Access Token: {access_token}")  # Debugging line

    try:
        response = requests.get(f'{FASTAPI_BASE_URL}/weather/current_weather?city={city}', headers=headers)
        if response.status_code == 200:
            weather_data = response.json()
            # print(f"🌤️ Weather Data: {weather_data}")  # Debugging line
        else:
            messages.error(request, "Failed to fetch current weather data.")
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error fetching weather data: {e}")
        # print(f"❌ Error fetching weather data: {e}")  # Debugging line

    try:
        forecast_response = requests.get(f'{FASTAPI_BASE_URL}/weather/forecast?city={city}', headers=headers)
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            # print(f"📅 Forecast Data: {forecast_data}")  # Debugging line
        else:
            messages.error(request, "Failed to fetch forecast data.")
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error fetching forecast data: {e}")

    return render(request, 'dashboard/home.html', {
        'weather_data': weather_data,
        'forecast_data': forecast_data
    })
