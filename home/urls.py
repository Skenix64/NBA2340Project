from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('players/', views.player_search_view, name='player_search'),
    path('teams/', views.team_search_view, name='team_search'),
]