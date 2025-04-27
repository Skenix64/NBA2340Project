from django.db import models

class Game(models.Model):
    GAME_TYPE_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
    ]

    date = models.DateField()
    time = models.TimeField(blank=True, null=True)  # ✅ Added Time Field!
    home_team = models.CharField(max_length=10)
    away_team = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    game_type = models.CharField(max_length=10, choices=GAME_TYPE_CHOICES, default='upcoming')

    # Only for completed games:
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    winner = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        time_display = self.time.strftime('%I:%M %p') if self.time else 'TBD'
        return f"{self.away_team} @ {self.home_team} on {self.date} at {time_display}"

