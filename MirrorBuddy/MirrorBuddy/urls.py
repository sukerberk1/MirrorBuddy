"""MirrorBuddy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from map.views import Home, map_finder, schedule_finder, schedule_specific
from spotted.views import spotted_view
from chatbot.views import chatbot_view

urlpatterns = [
    path('admin/', admin.site.urls),
    #map urls - mapfinder and all generic views down here
    path('', Home.as_view(), name='home'),
    path('map', map_finder, name='map-main'),
    # lesson plan views
    path('plan-lekcji', schedule_finder, name='schedule-finder'),
    path('plan-lekcji/<slug>', schedule_specific, name='schedule-specific'),

    #spotted view:
    path('spotted/', spotted_view, name='spottedapp'),

    #chatbot views:
    path('chatbot', chatbot_view, name='chatbot')
]
