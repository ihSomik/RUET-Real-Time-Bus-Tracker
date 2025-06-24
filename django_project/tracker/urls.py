from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='map'),
    path('api/bus-locations/', views.bus_locations, name='bus_locations'),
]

