from django.shortcuts import render
from django.http import JsonResponse
from .models import Bus

def map_view(request):
    return render(request, 'map.html')


def bus_locations(request):
    data = [
        {
            'number': bus.number,
            'lat': bus.current_lat,
            'lng': bus.current_lng
        }
        for bus in Bus.objects.all()
    ]
    return JsonResponse(data, safe=False)



from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the RUET Bus Tracker!")
