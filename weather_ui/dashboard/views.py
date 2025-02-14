from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests

@login_required
def home(request):
    weather_data = None
    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            # Replace with your FastAPI endpoint
            api_url = f'http://127.0.0.1:8000/weather/{city}'
            token = request.user.auth_token.key
            headers = {'Authorization': f'Token {token}'}
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                weather_data = response.json()
    return render(request, 'dashboard/home.html', {'weather_data': weather_data})


# New view for handling root URL '/'
def home_view(request):
    return render(request, 'dashboard/home.html')  # Ensure this template exists
