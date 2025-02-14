from django.contrib import admin
from django.urls import path, include
from dashboard.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Add this for root URL  
    path('accounts/', include('accounts.urls')),  # Includes URLs from the accounts app
    path('dashboard/', include('dashboard.urls')),  # Includes URLs from the dashboard app (if you have one)
]
