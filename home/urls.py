from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('players/', views.player_search_view, name='player_search'),
    path('teams/', views.team_search_view, name='team_search'),
    path('players/<int:player_id>/', views.player_detail_view, name='player_detail'),
    path('teams/<int:team_id>/', views.team_detail_view, name='team_detail'),

]