from django.shortcuts import render
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats


def homepage(request):
    return render(request, 'home/index.html')


from django.shortcuts import render
from nba_api.stats.static import players as nba_players


def player_search_view(request):
    query = request.GET.get('q', '')
    matched_players = []

    if query:
        all_players = nba_players.get_players()
        query_lower = query.lower()

        # Filter and reformat to dicts Django can use in template
        for p in all_players:
            if query_lower in p['full_name'].lower():
                matched_players.append({
                    'id': p['id'],
                    'full_name': p['full_name'],
                    'is_active': p['is_active']
                })

        # Debug print (optional)
        print("Matched players:", matched_players)

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


from django.shortcuts import render
from nba_api.stats.endpoints import playercareerstats

def player_detail_view(request, player_id):
    try:
        career = playercareerstats.PlayerCareerStats(player_id=int(player_id))
        stats_df = career.get_data_frames()[0]
        stats = stats_df.to_dict('records')
    except Exception as e:
        print("Error fetching stats:", e)
        stats = []

    context = {
        'player_id': player_id,
        'stats': stats,
    }
    return render(request, 'home/player_detail.html', context)




