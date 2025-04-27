from .favorite_behavior import FavoriteBehavior

class TeamFavoriteStrategy(FavoriteBehavior):
    def favorite(self, entity):
        print(f"Favoriting team: {entity.city} {entity.name}")

    def unfavorite(self, entity):
        print(f"Unfavoriting team: {entity.city} {entity.name}")
