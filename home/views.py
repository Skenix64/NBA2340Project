from django.shortcuts import render
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

from django.shortcuts import render
from nba_api.stats.static import players as nba_players
from NBA.models import Team, Player, TeamSeasonStats, PlayerSeasonStats
from NBA.services.entity_factory import NBAEntityFactory
from .models import Favorite


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

        # API players
        for p in all_players:
            if query_lower in p['full_name'].lower():
                player_dict = {
                    'id': p['id'],
                    'first_name': p['first_name'],
                    'last_name': p['last_name'],
                    'position': p.get('position', 'Unknown'),
                }
                entity = NBAEntityFactory.create_entity(player_dict, 'player')
                matched_players.append(entity)

        # Admin players
        admin_players = Player.objects.filter(name__icontains=query)
        for player in admin_players:
            matched_players.append(player)

    # Favorites
    favorites = set()
    if request.user.is_authenticated:
        favorites = set(Favorite.objects.filter(user=request.user, entity_type='player')
                        .values_list('entity_id', flat=True))

    context = {
        'query': query,
        'players': matched_players,
        'favorites': favorites
    }
    return render(request, 'home/player_search.html', context)



from nba_api.stats.static import teams as nba_teams

from nba_api.stats.static import teams as nba_teams
from .models import Favorite
from NBA.services.entity_factory import NBAEntityFactory

def team_search_view(request):
    query = request.GET.get('q', '')
    matched_teams = []

    # API teams
    if query:
        all_teams = nba_teams.get_teams()
        query_lower = query.lower()

        for t in all_teams:
            if query_lower in t['full_name'].lower():
                team_dict = {
                    'id': t['id'],
                    'full_name': t['full_name'],
                    'city': t.get('city', 'Unknown'),
                    'source': 'api'
                }
                entity = NBAEntityFactory.create_entity(team_dict, 'team')
                matched_teams.append(entity)

    # Admin teams
    admin_teams = Team.objects.filter(name__icontains=query)
    for team in admin_teams:
        team.source = 'admin'
        matched_teams.append(team)

    # Favorites
    favorites = set()
    if request.user.is_authenticated:
        favorites = set(Favorite.objects.filter(user=request.user, entity_type='team').values_list('entity_id', flat=True))

    context = {
        'query': query,
        'teams': matched_teams,
        'favorites': favorites
    }
    return render(request, 'home/team_search.html', context)






from django.shortcuts import render
from nba_api.stats.endpoints import playercareerstats

def player_detail_view(request, player_id):
    stats = []
    player_obj = None

    try:
        # Check for admin-entered player first
        admin_player = Player.objects.filter(id=player_id).first()

        if admin_player:
            player_obj = admin_player
            stats = PlayerSeasonStats.objects.filter(player=admin_player).order_by('season')
            # Format to match the template expectations (like API output)
            stats = [{
                'SEASON_ID': s.season,
                'TEAM_ABBREVIATION': s.player.team_name or 'N/A',
                'GP': s.games_played,
                'PTS': s.points,
                'REB': s.rebounds,
                'AST': s.assists
            } for s in stats]

        else:
            # Fallback to API
            all_players = nba_players.get_players()
            player_data = next((p for p in all_players if p['id'] == int(player_id)), None)

            if not player_data:
                raise ValueError("Player not found")

            player_obj = NBAEntityFactory.create_entity(player_data, 'player')
            career = playercareerstats.PlayerCareerStats(player_id=int(player_id))
            stats_df = career.get_data_frames()[0]
            stats = stats_df.to_dict('records')

    except Exception as e:
        print("Error in player_detail_view:", e)

    context = {
        'player_id': player_id,
        'player': player_obj,
        'stats': stats
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
    stats = []
    team_obj = None

    try:
        # Check if it's an admin-entered team
        admin_team = Team.objects.filter(id=team_id).first()

        if admin_team:
            team_obj = admin_team
            # Get and format admin stats
            stats = TeamSeasonStats.objects.filter(team=admin_team).order_by('season')
            stats = [{
                'YEAR': s.season,
                'TEAM_NAME': admin_team.name,
                'WINS': s.wins,
                'LOSSES': s.losses,
                'WIN_PCT': s.win_loss_pct
            } for s in stats]
        else:
            # Otherwise, use API
            all_teams = nba_teams.get_teams()
            team_data = next((t for t in all_teams if t['id'] == int(team_id)), None)

            if team_data:
                team_obj = NBAEntityFactory.create_entity(team_data, 'team')
                api_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=str(team_id))
                stats_df = api_stats.get_data_frames()[0]
                stats = stats_df.to_dict('records')

    except Exception as e:
        print("Error loading team stats:", e)

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
