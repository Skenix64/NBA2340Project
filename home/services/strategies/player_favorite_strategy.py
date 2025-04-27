from .favorite_behavior import FavoriteBehavior

class PlayerFavoriteStrategy(FavoriteBehavior):
    def favorite(self, entity):
        print(f"Favoriting player: {entity.first_name} {entity.last_name}")

    def unfavorite(self, entity):
        print(f"Unfavoriting player: {entity.first_name} {entity.last_name}")
