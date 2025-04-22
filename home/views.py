from django.shortcuts import render
from nba_api.stats.static import players


def homepage(request):
    return render(request, 'home/index.html')

def player_search_view(request):
    query = request.GET.get('q', '')
    matched_players = []

    if query:
        all_players = players.get_players()
        query_lower = query.lower()
        matched_players = [
            p for p in all_players if query_lower in p['full_name'].lower()
        ]

    context = {
        'query': query,
        'players': matched_players
    }
    return render(request, 'home/player_search.html', context)

def team_search_view(request):
    query = request.GET.get('q', '')
    teams = Team.objects.filter(name__icontains=query) if query else []

    context = {
        'query': query,
        'teams': teams,
    }
    return render(request, 'home/team_search.html', context)