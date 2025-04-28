from django.urls import path
from . import views

urlpatterns = [
    path('api/arenas/', views.arena_locations, name='arena_locations'),
    path('map/', views.map_page, name='map_page'),
]