from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TeamSeasonStats(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='seasons')
    season = models.CharField(max_length=9)  # e.g., "2023-24"
    wins = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()
    win_loss_pct = models.FloatField()

    def __str__(self):
        return f"{self.team.name} ({self.season})"

class Player(models.Model):
    name = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class PlayerSeasonStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='seasons')
    season = models.CharField(max_length=9)
    games_played = models.PositiveIntegerField()
    points = models.PositiveIntegerField()
    rebounds = models.PositiveIntegerField()
    assists = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.player.name} ({self.season})"
