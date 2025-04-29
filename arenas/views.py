from django.http import JsonResponse
from .models import Arena
from django.shortcuts import render

def arena_locations(request):
    arenas = list(Arena.objects.values())
    return JsonResponse(arenas, safe=False)

def map_page(request):
    return render(request, 'arenas/map.html')

def arena_list_api(request):
    arenas = Arena.objects.all()
    data = [
        {
            'name': arena.name,
            'team': arena.team,
            'latitude': arena.latitude,
            'longitude': arena.longitude
        }
        for arena in arenas
    ]
    return JsonResponse(data, safe=False)