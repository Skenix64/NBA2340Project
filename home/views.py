from django.shortcuts import render
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats


def homepage(request):
    return render(request, 'home/index.html')


from django.shortcuts import render
from nba_api.stats.static import players as nba_players


# def player_search_view(request):
#     query = request.GET.get('q', '')
#     matched_players = []
#
#     if query:
#         all_players = nba_players.get_players()
#         query_lower = query.lower()
#
#         # Filter and reformat to dicts Django can use in template
#         for p in all_players:
#             if query_lower in p['full_name'].lower():
#                 matched_players.append({
#                     'id': p['id'],
#                     'full_name': p['full_name'],
#                     'is_active': p['is_active']
#                 })
#
#         # Debug print (optional)
#         print("Matched players:", matched_players)
#
#     context = {
#         'query': query,
#         'players': matched_players
#     }
#     return render(request, 'home/player_search.html', context)

from NBA.services.entity_factory import NBAEntityFactory
from nba_api.stats.static import players as nba_players

def player_search_view(request):
    query = request.GET.get('q', '')
    matched_players = []

    if query:
        all_players = nba_players.get_players()
        query_lower = query.lower()

        for p in all_players:
            if query_lower in p['full_name'].lower():
                player_dict = {
                    'id': p['id'],
                    'first_name': p['first_name'],
                    'last_name': p['last_name'],
                    'position': p.get('position', 'Unknown')
                }
                entity = NBAEntityFactory.create_entity(player_dict, 'player')
                matched_players.append(entity)
    favorites = set()
    if request.user.is_authenticated:
        favorites = set(
            Favorite.objects.filter(user=request.user, entity_type='player').values_list('entity_id', flat=True))

    context = {
        'query': query,
        'players': matched_players,
        'favorites': favorites

    }
    return render(request, 'home/player_search.html', context)



# def team_search_view(request):
#     query = request.GET.get('q', '')
#     teams = Team.objects.filter(name__icontains=query) if query else []
#
#     context = {
#         'query': query,
#         'teams': teams,
#     }
#     return render(request, 'home/team_search.html', context)
from nba_api.stats.static import teams as nba_teams

def team_search_view(request):
    query = request.GET.get('q', '')
    matched_teams = []

    if query:
        all_teams = nba_teams.get_teams()
        query_lower = query.lower()

        for t in all_teams:
            if query_lower in t['full_name'].lower():
                team_dict = {
                    'id': t['id'],
                    'full_name': t['full_name'],
                    'city': t.get('city', 'Unknown')
                }
                entity = NBAEntityFactory.create_entity(team_dict, 'team')
                matched_teams.append(entity)

    context = {
        'query': query,
        'teams': matched_teams
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



from nba_api.stats.static import players, teams
from NBA.services.entity_factory import NBAEntityFactory

def factory_demo_view(request):
    query = request.GET.get('q', '')
    entities = []

    if query:
        player_data = players.get_players()
        team_data = teams.get_teams()

        for p in player_data:
            if query.lower() in p['full_name'].lower():
                player_dict = {
                    'id': p['id'],
                    'first_name': p['first_name'],
                    'last_name': p['last_name'],
                    'position': p.get('position', 'Unknown')
                }
                entity = NBAEntityFactory.create_entity(player_dict, 'player')
                entities.append(entity)

        for t in team_data:
            if query.lower() in t['full_name'].lower():
                team_dict = {
                    'id': t['id'],
                    'full_name': t['full_name'],
                    'city': t.get('city', 'Unknown')
                }
                entity = NBAEntityFactory.create_entity(team_dict, 'team')
                entities.append(entity)

    return render(request, 'home/factory_search.html', {'entities': entities, 'query': query})



from django.shortcuts import render
from nba_api.stats.endpoints import teamyearbyyearstats

from NBA.services.entity_factory import NBAEntityFactory
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats

def team_detail_view(request, team_id):
    try:
        # Get full team list and filter by ID
        all_teams = teams.get_teams()
        team_data = next((t for t in all_teams if t['id'] == team_id), None)

        if team_data is None:
            raise ValueError("Team not found")

        # Use factory to create a Team object
        team_obj = NBAEntityFactory.create_entity(team_data, 'team')

        # Get year-by-year stats
        stats = teamyearbyyearstats.TeamYearByYearStats(team_id=str(team_id)).get_data_frames()[0].to_dict('records')

    except Exception as e:
        print("Error:", e)
        stats = []
        team_obj = None

    context = {
        'team': team_obj,
        'stats': stats
    }
    return render(request, 'home/team_detail.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Favorite  # make sure you import your Favorite model

@login_required
def add_favorite(request):
    if request.method == 'POST':
        entity_id = request.POST.get('entity_id')
        entity_type = request.POST.get('entity_type')

        Favorite.objects.get_or_create(
            user=request.user,
            entity_id=entity_id,
            entity_type=entity_type
        )
    return redirect(request.META.get('HTTP_REFERER', '/'))



from NBA.services.entity_factory import NBAEntityFactory
from nba_api.stats.static import players, teams

@login_required
def remove_favorite(request):
    if request.method == 'POST':
        entity_id = request.POST.get('entity_id')
        entity_type = request.POST.get('entity_type')

        Favorite.objects.filter(
            user=request.user,
            entity_id=entity_id,
            entity_type=entity_type
        ).delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))



def favorite_list_view(request):
    favorites = Favorite.objects.filter(user=request.user)
    player_data = players.get_players()
    team_data = teams.get_teams()

    entities = []

    for fav in favorites:
        if fav.entity_type == 'player':
            data = next((p for p in player_data if p['id'] == int(fav.entity_id)), None)
            if data:
                entity = NBAEntityFactory.create_entity({
                    'id': data['id'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'position': data.get('position', 'Unknown')
                }, 'player')
                entities.append(entity)

        elif fav.entity_type == 'team':
            data = next((t for t in team_data if t['id'] == int(fav.entity_id)), None)
            if data:
                entity = NBAEntityFactory.create_entity({
                    'id': data['id'],
                    'full_name': data['full_name'],
                    'city': data.get('city', 'Unknown')
                }, 'team')
                entities.append(entity)

    return render(request, 'home/favorite_list.html', {'entities': entities})
