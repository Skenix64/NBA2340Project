from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Game
from .services.schedule_service import (
    get_api_games_data,
    format_api_game_result,
    get_api_past_games
)

def combine_manual_and_api_games(search_query=None):
    today = datetime.now().date()
    season_start = datetime(2024, 10, 23).date()

    manual_games_qs = Game.objects.filter(game_type='completed', date__gte=season_start, date__lt=today)

    if search_query:
        search_query = search_query.strip().upper()
        manual_games_qs = manual_games_qs.filter(
            home_team__icontains=search_query
        ) | manual_games_qs.filter(
            away_team__icontains=search_query
        )

    manual_games = [
        {
            'date': game.date,
            'formatted_date': game.date.strftime('%B %d, %Y'),
            'matchup': f"{game.away_team} @ {game.home_team}",
            'score': f"{game.away_score} - {game.home_score}",
            'winner': game.winner,
            'location': game.location,
            'source': 'manual'
        } for game in manual_games_qs
    ]

    api_games = get_api_past_games(search_query)
    combined_games = manual_games + api_games
    combined_games.sort(key=lambda x: x['date'], reverse=True)
    return combined_games

def get_yesterdays_games_combined():
    yesterday = datetime.now().date() - timedelta(days=1)

    manual_games_qs = Game.objects.filter(game_type='completed', date=yesterday)
    manual_games = [
        {
            'date': game.date,
            'formatted_date': game.date.strftime('%B %d, %Y'),
            'matchup': f"{game.away_team} @ {game.home_team}",
            'score': f"{game.away_score} - {game.home_score}",
            'winner': game.winner,
            'location': game.location,
            'source': 'manual'
        } for game in manual_games_qs
    ]

    api_games_data = get_api_games_data()
    api_games_yesterday = api_games_data[api_games_data['GAME_DATE'] == yesterday]

    api_games = []
    for game_id, game_data in api_games_yesterday.groupby('GAME_ID'):
        result = format_api_game_result(game_data)
        if result:
            api_games.append(result)

    return manual_games + api_games

def get_todays_games_combined():
    today = datetime.now().date()

    manual_games_qs = Game.objects.filter(game_type='completed', date=today)
    manual_games = [
        {
            'date': game.date,
            'formatted_date': game.date.strftime('%B %d, %Y'),
            'matchup': f"{game.away_team} @ {game.home_team}",
            'score': f"{game.away_score} - {game.home_score}",
            'winner': game.winner,
            'location': game.location,
            'source': 'manual'
        } for game in manual_games_qs
    ]

    api_games_data = get_api_games_data()
    api_games_today = api_games_data[api_games_data['GAME_DATE'] == today]

    api_games = []
    for game_id, game_data in api_games_today.groupby('GAME_ID'):
        result = format_api_game_result(game_data)
        if result:
            api_games.append(result)

    return manual_games + api_games

def schedule_view(request):
    search_query = request.GET.get('search', '').strip()
    search_query_upper = search_query.upper() if search_query else None
    search_results = combine_manual_and_api_games(search_query_upper) if search_query_upper else None

    yesterdays_games = get_yesterdays_games_combined()
    todays_games = get_todays_games_combined()
    upcoming_games = Game.objects.filter(game_type='upcoming').order_by('date')

    context = {
        'search_query': search_query,
        'search_results': search_results,
        'yesterdays_games': yesterdays_games,
        'todays_games': todays_games,
        'upcoming_games': upcoming_games,
    }
    return render(request, 'schedule/index.html', context)






