from nba_api.stats.endpoints import LeagueGameFinder
from datetime import datetime
import pandas as pd

# NBA Team Arena Lookup
TEAM_ARENAS = {
    'ATL': 'State Farm Arena',
    'BOS': 'TD Garden',
    'BKN': 'Barclays Center',
    'CHA': 'Spectrum Center',
    'CHI': 'United Center',
    'CLE': 'Rocket Arena',
    'DAL': 'American Airlines Center',
    'DEN': 'Ball Arena',
    'DET': 'Little Caesars Arena',
    'GSW': 'Chase Center',
    'HOU': 'Toyota Center',
    'IND': 'Gainbridge Fieldhouse',
    'LAC': 'Intuit Dome',
    'LAL': 'Crypto.com Arena',
    'MEM': 'FedExForum',
    'MIA': 'Kaseya Center',
    'MIL': 'Fiserv Forum',
    'MIN': 'Target Center',
    'NOP': 'Smoothie King Center',
    'NYK': 'Madison Square Garden',
    'OKC': 'Paycom Center',
    'ORL': 'Kia Center',
    'PHI': 'Wells Fargo Center',
    'PHX': 'PHX Arena',
    'POR': 'Moda Center',
    'SAC': 'Golden 1 Center',
    'SAS': 'Frost Bank Center',
    'TOR': 'Scotiabank Arena',
    'UTA': 'Delta Center',
    'WAS': 'Capital One Arena',
}

def get_api_games_data():
    gamefinder = LeagueGameFinder(season_nullable='2024-25', league_id_nullable='00')
    games = gamefinder.get_data_frames()[0]
    games['GAME_DATE'] = pd.to_datetime(games['GAME_DATE']).dt.date
    return games

def format_api_game_result(game_data):
    if len(game_data) != 2:
        return None  # Ensure both teams are present

    team1 = game_data.iloc[0]
    team2 = game_data.iloc[1]

    home_team = team1['TEAM_ABBREVIATION'] if 'vs.' in team1['MATCHUP'] else team2['TEAM_ABBREVIATION']
    away_team = team2['TEAM_ABBREVIATION'] if home_team == team1['TEAM_ABBREVIATION'] else team1['TEAM_ABBREVIATION']
    score = f"{team1['PTS']} - {team2['PTS']}"
    date = team1['GAME_DATE']

    # ✅ Use .get() to avoid KeyError on missing 'GAME_STATUS_TEXT'
    status = team1.get('GAME_STATUS_TEXT', 'Final')

    if "Final" in status:
        winner = team1['TEAM_ABBREVIATION'] if team1['WL'] == 'W' else team2['TEAM_ABBREVIATION']
    elif "Postponed" in status:
        winner = "Postponed"
    else:
        winner = status  # Display 'Halftime', '3rd Qtr', etc.

    location = TEAM_ARENAS.get(home_team, 'N/A')

    return {
        'date': date,
        'formatted_date': date.strftime('%B %d, %Y'),
        'matchup': f"{away_team} @ {home_team}",
        'score': score,
        'winner': winner,
        'location': location,
    }

def get_api_past_games(search_query=None):
    today = datetime.now().date()
    games = get_api_games_data()
    season_start = datetime(2024, 10, 23).date()
    past_games = games[
        (games['GAME_DATE'] < today) &
        (games['GAME_DATE'] >= season_start)
    ]

    if search_query:
        search_query = search_query.strip().upper()
        past_games = past_games[
            past_games['TEAM_ABBREVIATION'].str.upper().str.contains(search_query, na=False) |
            past_games['MATCHUP'].str.upper().str.contains(search_query, na=False)
        ]

    results = []
    for game_id, game_data in past_games.groupby('GAME_ID'):
        result = format_api_game_result(game_data)
        if result:
            results.append(result)
    return results
