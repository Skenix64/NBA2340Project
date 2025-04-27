from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('date', 'away_team', 'home_team', 'location', 'game_type', 'winner')
    list_filter = ('game_type', 'date')
