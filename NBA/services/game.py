class Game:
    def __init__(self, id, date, home_team, away_team):
        self.id = id
        self.date = date
        self.home_team = home_team
        self.away_team = away_team

    def __str__(self):
        return f"Game{{id={self.id}, date='{self.date}', homeTeam={self.home_team}, awayTeam={self.away_team}}}"
