from django.contrib import admin
from .models import Arena

@admin.register(Arena)
class ArenaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'team', 'latitude', 'longitude')