# check_scores.py
from nba_api.stats.endpoints import LeagueGameFinder
from datetime import datetime, timedelta
import pandas as pd

def main():
    # Load game data
    gamefinder = LeagueGameFinder(season_nullable='2024-25', league_id_nullable='00')
    games = gamefinder.get_data_frames()[0]
    games['GAME_DATE'] = pd.to_datetime(games['GAME_DATE']).dt.date

    # Filter for yesterday's games
    yesterday = datetime.now().date() - timedelta(days=1)
    yesterday_games = games[games['GAME_DATE'] == yesterday]

    # Print the results
    print(f"NBA Games from {yesterday.strftime('%B %d, %Y')}:\n")
    for game_id in yesterday_games['GAME_ID'].unique():
        game_data = yesterday_games[yesterday_games['GAME_ID'] == game_id]
        if len(game_data) == 2:  # Should be two rows: one for each team
            team1 = game_data.iloc[0]
            team2 = game_data.iloc[1]

            matchup = f"{team1['MATCHUP']}"
            score = f"{team1['PTS']} - {team2['PTS']}"
            winner = team1['TEAM_ABBREVIATION'] if team1['WL'] == 'W' else team2['TEAM_ABBREVIATION']

            print(f"{matchup}: {score} | Winner: {winner}")

if __name__ == "__main__":
    main()
