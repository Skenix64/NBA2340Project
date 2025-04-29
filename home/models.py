from django.db import models

# Create your models here.
from django.contrib.auth.models import User




class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entity_id = models.CharField(max_length=50)   # Player or Team ID
    entity_type = models.CharField(max_length=10) # 'player' or 'team'
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} favorites {self.entity_type} {self.entity_id}"
