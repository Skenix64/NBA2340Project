from django.contrib import admin
from .models import Team, TeamSeasonStats, Player, PlayerSeasonStats

class TeamSeasonInline(admin.TabularInline):
    model = TeamSeasonStats
    extra = 1

class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamSeasonInline]

class PlayerSeasonInline(admin.TabularInline):
    model = PlayerSeasonStats
    extra = 1

class PlayerAdmin(admin.ModelAdmin):
    inlines = [PlayerSeasonInline]

admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
