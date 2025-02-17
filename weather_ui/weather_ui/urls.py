from django.contrib import admin
from django.urls import path, include
from dashboard.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Add this for root URL  
    path('accounts/', include('accounts.urls')),  # Includes URLs from the accounts app
    path('dashboard/', include('dashboard.urls')),  # Includes URLs from the dashboard app (if you have one)
]
