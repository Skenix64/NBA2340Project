import requests

class NBAStatsService:
    API_BASE_URL = "https://api-nba-v1.p.rapidapi.com/"
    API_KEY = "bd2c81e03cmsh8a8d7dffc4442a0p1b8612jsn20a02d70f095"

    HEADERS = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    def get_player_info(self, player_name):
        response = requests.get(f"{self.API_BASE_URL}players?search={player_name}", headers=self.HEADERS)
        response.raise_for_status()
        return response.text

    def get_player_stats(self, player_id):
        response = requests.get(f"{self.API_BASE_URL}players/statistics?player={player_id}", headers=self.HEADERS)
        response.raise_for_status()
        return response.text

    def get_team_stats(self, team_id):
        response = requests.get(f"{self.API_BASE_URL}teams?id={team_id}", headers=self.HEADERS)
        response.raise_for_status()
        return response.text

    def get_game_stats(self, game_id):
        response = requests.get(f"{self.API_BASE_URL}games?id={game_id}", headers=self.HEADERS)
        response.raise_for_status()
        return response.text
