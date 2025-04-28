from django.http import JsonResponse
from .models import Arena
from django.shortcuts import render

def arena_locations(request):
    arenas = list(Arena.objects.values())
    return JsonResponse(arenas, safe=False)

def map_page(request):
    return render(request, 'arenas/map.html')